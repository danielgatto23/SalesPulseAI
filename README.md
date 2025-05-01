# Sistema de Insights de Vendas

Sistema inteligente para previsão de vendas e recomendação de produtos, com envio automatizado de insights via Telegram.

## 🚀 Funcionalidades

- **Ingestão de Dados**: Suporte para arquivos CSV, Excel, JSON e conexão com banco de dados SQL
- **Modelagem Preditiva**: Previsão de vendas usando Prophet e XGBoost
- **Recomendação de Produtos**: Baseada em filtragem colaborativa e regras de associação
- **Personalização por Persona**: Insights adaptados para diferentes perfis de usuário
- **Geração de Insights**: Utilizando a API Gemini para linguagem natural
- **Envio Automatizado**: Distribuição de insights via Telegram com base em regras configuráveis

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Conta no Google Cloud para API Gemini
- Bot do Telegram configurado

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sales-insights-ai.git
cd sales-insights-ai
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

5. Configure as variáveis de ambiente no arquivo `.env`:
- `GEMINI_API_KEY`: Sua chave da API Gemini
- `TELEGRAM_BOT_TOKEN`: Token do seu bot do Telegram
- `DB_CONNECTION_STRING`: String de conexão com o banco de dados (se aplicável)

## 🛠️ Estrutura do Projeto

```
sales-insights-ai/
├── agents/                  # Agentes CrewAI
├── config/                  # Configurações
├── data/                    # Dados de exemplo
├── models/                  # Modelos de ML
├── templates/               # Templates de relatórios
├── utils/                   # Utilitários
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
└── README.md              # Documentação
```

## 📝 Configuração de Usuários

1. Crie um arquivo de configuração para cada usuário em `config/user_configs/`:
```json
{
    "usuario_id": "12345",
    "persona": "diretor_comercial",
    "frequencia_envio": "semanal",
    "tipo_conteudo": ["tendencias", "anomalias", "top_produtos"],
    "horario_preferido": "08:30",
    "formato_preferido": "resumo_executivo"
}
```

2. As personas disponíveis são:
- `diretor_comercial`: Visão macro e resumo executivo
- `analista_de_vendas`: Análise detalhada e técnica
- `representante_de_campo`: Foco em metas e oportunidades

## 🚀 Executando o Sistema

1. Inicie o sistema:
```bash
python main.py
```

2. O sistema irá:
- Carregar as configurações dos usuários
- Agendar os envios de acordo com as preferências
- Processar os dados e gerar insights
- Enviar os relatórios via Telegram

## 📊 Dados de Exemplo

O diretório `data/` contém arquivos de exemplo nos formatos suportados:
- `sample_sales_data.csv`: Dados de vendas em formato CSV
- `sample_sales_data.xlsx`: Dados de vendas em formato Excel
- `sample_sales_data.json`: Dados de vendas em formato JSON

## 🔍 Monitoramento

O sistema registra logs de execução, incluindo:
- Carregamento de dados
- Geração de previsões
- Envio de mensagens
- Erros e exceções

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📧 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/sales-insights-ai](https://github.com/seu-usuario/sales-insights-ai) 