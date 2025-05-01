import json
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class InsightManager:
    def __init__(self, config_path: str = "config/user_configs/default_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carrega a configuração do arquivo JSON."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {str(e)}")
            raise
    
    def get_available_insights(self, persona: str) -> List[Dict[str, Any]]:
        """Retorna os insights disponíveis para uma persona específica."""
        try:
            return self.config["configuracoes_persona"][persona]["insights_disponiveis"]
        except KeyError:
            logger.error(f"Persona '{persona}' não encontrada")
            return []
    
    def select_insights(self, persona: str, selected_insights: List[str]) -> bool:
        """Permite ao usuário selecionar os insights que deseja receber."""
        try:
            available_insights = self.get_available_insights(persona)
            if not available_insights:
                return False
            
            # Valida se todos os insights selecionados existem
            available_names = [insight["nome"] for insight in available_insights]
            for insight_name in selected_insights:
                if insight_name not in available_names:
                    logger.error(f"Insight '{insight_name}' não disponível para a persona '{persona}'")
                    return False
            
            # Atualiza a configuração
            self.config["persona"] = persona
            self.config["tipo_conteudo"] = selected_insights
            
            # Salva a configuração atualizada
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Insights selecionados para {persona}: {selected_insights}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao selecionar insights: {str(e)}")
            return False
    
    def get_current_selection(self) -> Dict[str, Any]:
        """Retorna a seleção atual de insights."""
        return {
            "persona": self.config["persona"],
            "selected_insights": self.config["tipo_conteudo"]
        }
    
    def list_insights_by_persona(self, persona: str) -> None:
        """Lista todos os insights disponíveis para uma persona."""
        insights = self.get_available_insights(persona)
        if not insights:
            print(f"Nenhum insight disponível para a persona '{persona}'")
            return
        
        print(f"\nInsights disponíveis para {persona}:")
        for i, insight in enumerate(insights, 1):
            print(f"\n{i}. {insight['nome']}")
            print(f"   Descrição: {insight['descricao']}")
            print(f"   Frequência: {insight['frequencia']}")
            print(f"   Nível de detalhe: {insight['nivel_detalhe']}")
            print(f"   Métricas: {', '.join(insight['metricas'])}")
            print(f"   Segmentos: {', '.join(insight['segmentos'])}")

def main():
    """Função principal para interação com o usuário."""
    manager = InsightManager()
    
    print("Bem-vindo ao Sistema de Seleção de Insights!")
    print("\nPersonas disponíveis:")
    print("1. Diretor Comercial")
    print("2. Analista de Vendas")
    print("3. Representante de Campo")
    
    while True:
        try:
            choice = input("\nEscolha uma persona (1-3) ou 'q' para sair: ")
            if choice.lower() == 'q':
                break
            
            personas = {
                "1": "diretor_comercial",
                "2": "analista_de_vendas",
                "3": "representante_de_campo"
            }
            
            if choice not in personas:
                print("Opção inválida!")
                continue
            
            persona = personas[choice]
            manager.list_insights_by_persona(persona)
            
            print("\nDigite os números dos insights que deseja receber (separados por vírgula):")
            selected = input("> ").strip().split(',')
            selected = [s.strip() for s in selected]
            
            available_insights = manager.get_available_insights(persona)
            selected_names = [available_insights[int(s)-1]["nome"] for s in selected if s.isdigit()]
            
            if manager.select_insights(persona, selected_names):
                print("\nSeleção atualizada com sucesso!")
                current = manager.get_current_selection()
                print(f"Persona: {current['persona']}")
                print(f"Insights selecionados: {', '.join(current['selected_insights'])}")
            else:
                print("\nErro ao atualizar seleção. Tente novamente.")
            
        except Exception as e:
            print(f"\nErro: {str(e)}")
            continue

if __name__ == "__main__":
    main() 