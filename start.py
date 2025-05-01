import os
import sys
import subprocess
import shutil
from pathlib import Path
import logging
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sales_insights.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SetupManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_dir = self.base_dir / "config"
        self.data_dir = self.base_dir / "data"
        self.templates_dir = self.base_dir / "templates"
        
    def check_python_version(self):
        """Verifica versão do Python."""
        if sys.version_info < (3, 8):
            logger.error("Python 3.8 ou superior é necessário")
            sys.exit(1)
        logger.info(f"Python versão {sys.version_info.major}.{sys.version_info.minor} detectada")
    
    def setup_virtual_env(self):
        """Configura ambiente virtual."""
        venv_path = self.base_dir / "venv"
        if not venv_path.exists():
            logger.info("Criando ambiente virtual...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
        
        # Ativa o ambiente virtual
        if sys.platform == "win32":
            activate_script = venv_path / "Scripts" / "activate.bat"
            subprocess.run([str(activate_script)], shell=True)
        else:
            activate_script = venv_path / "bin" / "activate"
            subprocess.run(f"source {activate_script}", shell=True)
        
        logger.info("Ambiente virtual configurado")
    
    def install_dependencies(self):
        """Instala dependências."""
        logger.info("Instalando dependências...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Dependências instaladas")
    
    def setup_directories(self):
        """Cria estrutura de diretórios necessária."""
        directories = [
            self.config_dir / "user_configs",
            self.data_dir,
            self.templates_dir,
            self.base_dir / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Diretório {directory} verificado")
    
    def setup_env_file(self):
        """Configura arquivo .env."""
        env_path = self.base_dir / ".env"
        if not env_path.exists():
            logger.info("Criando arquivo .env...")
            with open(env_path, "w") as f:
                f.write("""# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Configurações do Sistema
LOG_LEVEL=INFO
DATA_DIR=data/
CONFIG_DIR=config/
TEMPLATES_DIR=templates/

# Configurações do Banco de Dados (opcional)
DB_CONNECTION_STRING=postgresql://user:password@localhost:5432/database
""")
            logger.warning("Arquivo .env criado. Por favor, configure suas chaves de API")
    
    def setup_sample_data(self):
        """Configura dados de exemplo."""
        sample_data_path = self.data_dir / "sample_sales_data.csv"
        if not sample_data_path.exists():
            logger.info("Criando dados de exemplo...")
            import pandas as pd
            import numpy as np
            
            # Gera dados de exemplo
            dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
            n_dates = len(dates)
            
            data = {
                'date': np.repeat(dates, 10),
                'product_id': np.tile(range(1, 11), n_dates),
                'product_name': np.tile([f'Produto {i}' for i in range(1, 11)], n_dates),
                'category': np.tile(['Eletrônicos', 'Roupas', 'Alimentos', 'Casa', 'Esportes'] * 2, n_dates),
                'price': np.random.uniform(10, 1000, n_dates * 10),
                'quantity': np.random.randint(1, 100, n_dates * 10),
                'user_id': np.random.randint(1, 1000, n_dates * 10),
                'rating': np.random.randint(1, 5, n_dates * 10)
            }
            
            df = pd.DataFrame(data)
            df.to_csv(sample_data_path, index=False)
            logger.info("Dados de exemplo criados")
    
    def setup_templates(self):
        """Configura templates padrão."""
        templates = {
            "diretor_comercial.txt": """# Resumo Executivo de Vendas

## Visão Geral
{visao_geral}

## KPIs Principais
- Total de Vendas: {total_vendas}
- Crescimento: {crescimento}%
- Produtos Mais Vendidos: {top_produtos}

## Insights Principais
{insights}

## Previsões
- Próximos 30 dias: {previsao_30_dias}
- Tendências: {tendencias}

## Recomendações
{recomendacoes}

## Alertas
{alertas}

## Próximos Passos
{proximos_passos}
""",
            "analista_de_vendas.txt": """# Análise Detalhada de Vendas

## Desempenho por Segmento
{desempenho_por_segmento}

## Tendências de Vendas
{tendencias}

## Análise de Produtos
### Top Produtos
{top_produtos}

### Produtos com Baixo Desempenho
{produtos_baixo_desempenho}

### Oportunidades de Crescimento
{oportunidades}

## Análise de Anomalias
{anomalias}

## Insights Detalhados
{insights}

## Previsões
### Prophet
{previsao_prophet}

### XGBoost
{previsao_xgboost}

## Recomendações Técnicas
{recomendacoes_tecnicas}

## Ações Recomendadas
{acoes_recomendadas}
""",
            "representante_de_campo.txt": """# Relatório Diário de Campo

## Metas do Dia
{metas_do_dia}

## Desempenho Atual
{desempenho_atual}

## Produtos em Destaque
{produtos_destaque}

## Oportunidades de Venda
{oportunidades}

## Tendências Locais
{tendencias_locais}

## Insights sobre Clientes
{insights_clientes}

## Lista de Tarefas
{tarefas}

## Dicas de Vendas
{dicas}

## Alertas Importantes
{alertas}

## Próximas Visitas
{proximas_visitas}
"""
        }
        
        for template_name, content in templates.items():
            template_path = self.templates_dir / template_name
            if not template_path.exists():
                logger.info(f"Criando template {template_name}...")
                with open(template_path, "w", encoding="utf-8") as f:
                    f.write(content)
    
    def setup_default_config(self):
        """Configura arquivo de configuração padrão."""
        config_path = self.config_dir / "user_configs" / "default_config.json"
        if not config_path.exists():
            logger.info("Criando configuração padrão...")
            import json
            
            default_config = {
                "usuario_id": "default",
                "persona": "diretor_comercial",
                "frequencia_envio": "diario",
                "horario_preferido": "08:30",
                "formato_preferido": "resumo_executivo",
                "preferencias_analise": {
                    "previsao_vendas": {
                        "horizonte": 30,
                        "metodo": "prophet",
                        "nivel_detalhe": "alto",
                        "metricas": ["volume", "receita", "margem"],
                        "segmentos": ["geral", "categoria", "produto"]
                    },
                    "recomendacao_produtos": {
                        "metodo": "hibrido",
                        "filtros": {
                            "categoria": True,
                            "preco": True,
                            "desempenho": True
                        },
                        "quantidade": 5,
                        "periodo_analise": 90
                    }
                },
                "alertas": {
                    "anomalias": True,
                    "tendencias": True,
                    "metas": True,
                    "threshold_anomalia": 0.2
                },
                "tipo_conteudo": [
                    "tendencias",
                    "anomalias",
                    "top_produtos",
                    "previsoes",
                    "recomendacoes"
                ]
            }
            
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            logger.info("Configuração padrão criada")
    
    def run(self):
        """Executa todo o processo de setup."""
        try:
            logger.info("Iniciando configuração do sistema...")
            
            self.check_python_version()
            self.setup_virtual_env()
            self.install_dependencies()
            self.setup_directories()
            self.setup_env_file()
            self.setup_sample_data()
            self.setup_templates()
            self.setup_default_config()
            
            logger.info("Configuração concluída com sucesso!")
            logger.info("Por favor, configure suas chaves de API no arquivo .env")
            logger.info("Execute 'python main.py' para iniciar o sistema")
            
        except Exception as e:
            logger.error(f"Erro durante a configuração: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    setup_manager = SetupManager()
    setup_manager.run() 