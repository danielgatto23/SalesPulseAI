# SalesForce.AI
```
   _____       __    __    _____    _____    _____    _____    _____    _____    _____    _____
  / ____|     /  |  /  |  / ____|  / ____|  / ____|  / ____|  / ____|  / ____|  / ____|  / ____|
 | (___      / / | / / | | (___   | (___   | (___   | (___   | (___   | (___   | (___   | (___  
  \___ \    / /| |/ /| |  \___ \   \___ \   \___ \   \___ \   \___ \   \___ \   \___ \   \___ \ 
  ____) |  / / |   | |  ____) |  ____) |  ____) |  ____) |  ____) |  ____) |  ____) |  ____) |
 |_____/  /_/  |___| | |_____/  |_____/  |_____/  |_____/  |_____/  |_____/  |_____/  |_____/ 
```

# 🤖 Sistema de Insights de Vendas com Multi-Agentes

Sistema inteligente de análise de vendas que utiliza uma equipe de agentes especializados trabalhando em conjunto para fornecer insights precisos e recomendações personalizadas.

## 🌟 Destaques

- **Arquitetura Multi-Agentes**: Cada aspecto do sistema é gerenciado por um agente especializado
- **Análise em Tempo Real**: Processamento contínuo de dados para insights atualizados
- **Personalização por Perfil**: Relatórios adaptados para diferentes personas
- **Integração com IA**: Utiliza modelos avançados de machine learning e processamento de linguagem natural
- **Automação Completa**: Do processamento de dados ao envio de relatórios

## 👥 Equipe de Agentes Especializados

### 📊 Agente de Ingestão de Dados
- Coleta dados de múltiplas fontes (CSV, Excel, JSON, SQL)
- Realiza limpeza e normalização automática
- Detecta e corrige anomalias nos dados
- Mantém pipeline de dados em tempo real

### 🧠 Agente de Modelagem
- Gera previsões de vendas usando Prophet e XGBoost
- Implementa sistema de recomendação com filtragem colaborativa
- Identifica padrões e tendências
- Ajusta modelos automaticamente baseado em feedback

### 💡 Agente de Geração de Insights
- Utiliza IA generativa (API Gemini) para análises em linguagem natural
- Adapta o tom e profundidade das análises por perfil
- Gera insights acionáveis e recomendações estratégicas
- Prioriza informações relevantes para cada usuário

### 📱 Agente de Distribuição Telegram
- Envia relatórios personalizados via Telegram
- Gerencia agendamentos e frequência de envios
- Formata mensagens para melhor visualização mobile
- Permite interação e feedback dos usuários

## 🎯 Personas e Relatórios Personalizados

### 👔 Diretor Comercial
- Visão macro do negócio
- KPIs principais e tendências
- Alertas estratégicos
- Recomendações de alto nível

### 📈 Analista de Vendas
- Análise detalhada de dados
- Insights técnicos aprofundados
- Previsões e modelagens
- Oportunidades de otimização

### 🚀 Representante de Campo
- Metas e desempenho diário
- Oportunidades de venda
- Insights sobre clientes
- Recomendações táticas

## 🛠️ Tecnologias Utilizadas

- **Machine Learning**: Prophet, XGBoost, Scikit-learn
- **IA Generativa**: Google Gemini API
- **Processamento de Dados**: Pandas, NumPy
- **Automação**: CrewAI, APScheduler
- **Comunicação**: Python Telegram Bot API

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

4. Configure as variáveis de ambiente no arquivo `.env`:
```
GEMINI_API_KEY=sua-chave-aqui
TELEGRAM_BOT_TOKEN=seu-token-aqui
```

## 📊 Exemplo de Uso

1. Configure os perfis de usuário em `config/user_configs/`
2. Adicione suas fontes de dados em `data/`
3. Execute o sistema:
```bash
python main.py
```

O sistema iniciará automaticamente:
- 🤖 Ativando todos os agentes
- 📊 Processando dados em tempo real
- 🧠 Gerando insights personalizados
- 📱 Enviando relatórios via Telegram

## 📈 Benefícios

- **Economia de Tempo**: Automação de análises complexas
- **Insights Acionáveis**: Recomendações práticas e contextualizadas
- **Personalização**: Informações relevantes para cada perfil
- **Monitoramento Contínuo**: Alertas e atualizações em tempo real
- **Escalabilidade**: Arquitetura modular e extensível

## 🔍 Monitoramento

O sistema mantém logs detalhados de todas as operações:
- Atividades dos agentes
- Processamento de dados
- Geração de insights
- Envio de mensagens
- Erros e exceções

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📧 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/sales-insights-ai](https://github.com/seu-usuario/sales-insights-ai) 