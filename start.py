import os
import sys
from pathlib import Path
import subprocess

def setup_environment():
    """Configura o ambiente inicial."""
    # Criar diretórios necessários
    directories = ['data', 'config/user_configs', 'logs']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Verificar se o arquivo .env existe
    if not Path('.env').exists():
        print("Arquivo .env não encontrado. Copiando .env.example...")
        if Path('.env.example').exists():
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
        else:
            print("Erro: Arquivo .env.example não encontrado!")
            sys.exit(1)
    
    # Verificar se o arquivo de configuração padrão existe
    if not Path('config/user_configs/default_user.json').exists():
        print("Arquivo de configuração padrão não encontrado. Criando...")
        # O arquivo já foi criado anteriormente

def install_dependencies():
    """Instala as dependências necessárias."""
    print("Instalando dependências...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def main():
    """Função principal."""
    print("Iniciando configuração do ambiente...")
    setup_environment()
    install_dependencies()
    
    print("\nAmbiente configurado com sucesso!")
    print("\nPara executar o sistema, use:")
    print("python main.py")
    print("\nCertifique-se de configurar suas credenciais no arquivo .env:")
    print("- GEMINI_API_KEY: Sua chave da API Gemini")
    print("- TELEGRAM_BOT_TOKEN: Token do seu bot do Telegram")

if __name__ == "__main__":
    main() 