from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

class ProductRecommendationModel:
    def __init__(self):
        self.user_similarity_matrix = None
        self.item_similarity_matrix = None
        self.frequent_itemsets = None
        self.association_rules = None
        
    def prepare_collaborative_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for collaborative filtering."""
        # Create user-item matrix
        user_item_matrix = df.pivot(
            index='user_id',
            columns='product_id',
            values='rating'
        ).fillna(0)
        
        return user_item_matrix
        
    def prepare_association_data(self, df: pd.DataFrame) -> List[List[str]]:
        """Prepare data for association rules mining."""
        # Group products by user
        user_products = df.groupby('user_id')['product_id'].apply(list).tolist()
        
        # Convert to transaction format
        te = TransactionEncoder()
        te_ary = te.fit(user_products).transform(user_products)
        return pd.DataFrame(te_ary, columns=te.columns_)
        
    def generate_collaborative_recommendations(self, user_item_matrix: pd.DataFrame, user_id: str, n_recommendations: int = 5) -> List[Dict[str, Any]]:
        """Generate recommendations using collaborative filtering."""
        try:
            # Calculate user similarity
            self.user_similarity_matrix = cosine_similarity(user_item_matrix)
            self.item_similarity_matrix = cosine_similarity(user_item_matrix.T)
            
            # Get user's ratings
            user_ratings = user_item_matrix.loc[user_id]
            
            # Find similar users
            user_idx = user_item_matrix.index.get_loc(user_id)
            similar_users = np.argsort(self.user_similarity_matrix[user_idx])[::-1][1:6]
            
            # Get recommendations from similar users
            recommendations = []
            for similar_user_idx in similar_users:
                similar_user_id = user_item_matrix.index[similar_user_idx]
                similar_user_ratings = user_item_matrix.loc[similar_user_id]
                
                # Find products that similar user liked but current user hasn't rated
                new_products = similar_user_ratings[user_ratings == 0]
                if not new_products.empty:
                    top_product = new_products.idxmax()
                    recommendations.append({
                        "product_id": top_product,
                        "score": float(similar_user_ratings[top_product]),
                        "type": "collaborative"
                    })
            
            return sorted(recommendations, key=lambda x: x["score"], reverse=True)[:n_recommendations]
            
        except Exception as e:
            print(f"Error in collaborative filtering: {str(e)}")
            return []
            
    def generate_association_recommendations(self, transactions: pd.DataFrame, user_id: str, n_recommendations: int = 5) -> List[Dict[str, Any]]:
        """Generate recommendations using association rules."""
        try:
            # Generate frequent itemsets
            self.frequent_itemsets = apriori(transactions, min_support=0.1, use_colnames=True)
            
            # Generate association rules
            self.association_rules = association_rules(
                self.frequent_itemsets,
                metric="lift",
                min_threshold=1.0
            )
            
            # Get user's purchased products
            user_products = set(transactions.columns[transactions.loc[user_id]])
            
            # Find recommendations based on association rules
            recommendations = []
            for _, rule in self.association_rules.iterrows():
                antecedents = set(rule['antecedents'])
                consequents = set(rule['consequents'])
                
                # If user has purchased all antecedents but not consequents
                if antecedents.issubset(user_products) and not consequents.issubset(user_products):
                    for product in consequents - user_products:
                        recommendations.append({
                            "product_id": product,
                            "score": float(rule['lift']),
                            "type": "association"
                        })
            
            return sorted(recommendations, key=lambda x: x["score"], reverse=True)[:n_recommendations]
            
        except Exception as e:
            print(f"Error in association rules: {str(e)}")
            return []
            
    def generate_recommendations(self, df: pd.DataFrame, user_id: str) -> Dict[str, Any]:
        """Generate recommendations using both methods."""
        try:
            # Prepare data
            user_item_matrix = self.prepare_collaborative_data(df)
            transactions = self.prepare_association_data(df)
            
            # Generate recommendations
            collaborative_recs = self.generate_collaborative_recommendations(user_item_matrix, user_id)
            association_recs = self.generate_association_recommendations(transactions, user_id)
            
            # Combine and deduplicate recommendations
            all_recommendations = collaborative_recs + association_recs
            seen_products = set()
            final_recommendations = []
            
            for rec in all_recommendations:
                if rec["product_id"] not in seen_products:
                    seen_products.add(rec["product_id"])
                    final_recommendations.append(rec)
            
            return {
                "status": "success",
                "recommendations": final_recommendations[:5]  # Return top 5 recommendations
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            } 