from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import logging

class ProductRecommendationModel:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.user_similarity_matrix = None
        self.item_similarity_matrix = None
        self.frequent_itemsets = None
        self.association_rules = None
        
    def prepare_collaborative_data(self, df: pd.DataFrame, persona_config: Dict) -> pd.DataFrame:
        """Prepara matriz usuário-item para filtragem colaborativa."""
        try:
            # Seleciona período de análise baseado na configuração
            period = persona_config['recomendacao_produtos']['periodo_analise']
            end_date = df['date'].max()
            start_date = end_date - pd.Timedelta(days=period)
            
            # Filtra dados pelo período
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
            # Aplica filtros configurados
            if persona_config['recomendacao_produtos']['filtros']['preco']:
                df = df[df['price'] <= df['price'].quantile(0.95)]
            
            if persona_config['recomendacao_produtos']['filtros']['desempenho']:
                df = df[df['quantity'] > 0]
            
            # Cria matriz usuário-item
            user_item_matrix = df.pivot_table(
                index='user_id',
                columns='product_id',
                values='rating',
                fill_value=0
            )
            
            return user_item_matrix
        except Exception as e:
            self.logger.error(f"Erro ao preparar dados colaborativos: {str(e)}")
            raise
        
    def prepare_association_data(self, df: pd.DataFrame, persona_config: Dict) -> pd.DataFrame:
        """Prepara dados para regras de associação."""
        try:
            # Seleciona período de análise
            period = persona_config['recomendacao_produtos']['periodo_analise']
            end_date = df['date'].max()
            start_date = end_date - pd.Timedelta(days=period)
            
            # Filtra dados pelo período
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
            # Aplica filtros configurados
            if persona_config['recomendacao_produtos']['filtros']['categoria']:
                df = df.groupby(['transaction_id', 'category'])['product_id'].count().unstack().fillna(0)
            else:
                df = df.groupby(['transaction_id', 'product_id'])['quantity'].sum().unstack().fillna(0)
            
            # Binariza os dados
            df = (df > 0).astype(int)
            
            return df
        except Exception as e:
            self.logger.error(f"Erro ao preparar dados de associação: {str(e)}")
            raise
        
    def generate_collaborative_recommendations(
        self, 
        user_item_matrix: pd.DataFrame,
        user_id: str,
        persona_config: Dict
    ) -> List[Dict]:
        """Gera recomendações baseadas em filtragem colaborativa."""
        try:
            if user_id not in user_item_matrix.index:
                return []
            
            # Calcula similaridade entre usuários
            user_similarity = cosine_similarity(user_item_matrix)
            user_similarity = pd.DataFrame(
                user_similarity,
                index=user_item_matrix.index,
                columns=user_item_matrix.index
            )
            
            # Obtém usuários similares
            similar_users = user_similarity[user_id].sort_values(ascending=False)[1:6]
            
            # Obtém produtos não avaliados pelo usuário
            user_ratings = user_item_matrix.loc[user_id]
            unrated_products = user_ratings[user_ratings == 0].index
            
            # Calcula previsão de avaliação
            predictions = []
            for product in unrated_products:
                product_ratings = user_item_matrix[product]
                weighted_sum = 0
                similarity_sum = 0
                
                for similar_user, similarity in similar_users.items():
                    if product_ratings[similar_user] > 0:
                        weighted_sum += similarity * product_ratings[similar_user]
                        similarity_sum += similarity
                
                if similarity_sum > 0:
                    predictions.append({
                        'product_id': product,
                        'score': weighted_sum / similarity_sum
                    })
            
            # Ordena e retorna top N recomendações
            predictions.sort(key=lambda x: x['score'], reverse=True)
            return predictions[:persona_config['recomendacao_produtos']['quantidade']]
        except Exception as e:
            self.logger.error(f"Erro ao gerar recomendações colaborativas: {str(e)}")
            raise
        
    def generate_association_recommendations(
        self,
        transactions: pd.DataFrame,
        persona_config: Dict
    ) -> List[Dict]:
        """Gera recomendações baseadas em regras de associação."""
        try:
            # Encontra itemsets frequentes
            frequent_itemsets = apriori(
                transactions,
                min_support=0.01,
                use_colnames=True
            )
            
            # Gera regras de associação
            rules = association_rules(
                frequent_itemsets,
                metric="lift",
                min_threshold=1
            )
            
            # Filtra e ordena regras
            rules = rules[
                (rules['confidence'] > 0.5) &
                (rules['lift'] > 1)
            ].sort_values('lift', ascending=False)
            
            # Formata recomendações
            recommendations = []
            for _, rule in rules.head(persona_config['recomendacao_produtos']['quantidade']).iterrows():
                recommendations.append({
                    'antecedents': list(rule['antecedents']),
                    'consequents': list(rule['consequents']),
                    'confidence': rule['confidence'],
                    'lift': rule['lift']
                })
            
            return recommendations
        except Exception as e:
            self.logger.error(f"Erro ao gerar recomendações de associação: {str(e)}")
            raise
        
    def generate_recommendations(
        self,
        df: pd.DataFrame,
        persona_config: Dict,
        user_id: Optional[str] = None
    ) -> List[Dict]:
        """Gera recomendações usando o método especificado na configuração."""
        try:
            method = persona_config['recomendacao_produtos']['metodo']
            
            if method == 'colaborativo':
                user_item_matrix = self.prepare_collaborative_data(df, persona_config)
                return self.generate_collaborative_recommendations(
                    user_item_matrix,
                    user_id,
                    persona_config
                )
            elif method == 'associacao':
                transactions = self.prepare_association_data(df, persona_config)
                return self.generate_association_recommendations(
                    transactions,
                    persona_config
                )
            elif method == 'hibrido':
                # Combina ambos os métodos
                collaborative_recs = self.generate_collaborative_recommendations(
                    self.prepare_collaborative_data(df, persona_config),
                    user_id,
                    persona_config
                )
                association_recs = self.generate_association_recommendations(
                    self.prepare_association_data(df, persona_config),
                    persona_config
                )
                
                # Combina e ordena recomendações
                all_recs = collaborative_recs + association_recs
                all_recs.sort(key=lambda x: x.get('score', x.get('lift', 0)), reverse=True)
                return all_recs[:persona_config['recomendacao_produtos']['quantidade']]
            else:
                raise ValueError(f"Método de recomendação inválido: {method}")
        except Exception as e:
            self.logger.error(f"Erro ao gerar recomendações: {str(e)}")
            raise 