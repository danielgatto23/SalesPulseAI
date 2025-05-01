from typing import Dict, Any
from crewai import Agent
from telegram import Bot
from telegram.error import TelegramError
import asyncio
from pathlib import Path
import json

class TelegramDispatchAgent(Agent):
    def __init__(self, telegram_api):
        super().__init__(
            role="Telegram Dispatcher",
            goal="Enviar insights via Telegram de acordo com as preferências do usuário",
            backstory="""Você é um especialista em comunicação via Telegram, 
            responsável por entregar insights de forma clara e eficiente."""
        )
        self.telegram_api = telegram_api
        self.config_dir = Path("config")
        
    def load_user_config(self, user_id: str) -> Dict[str, Any]:
        """Load user configuration from JSON file."""
        config_path = self.config_dir / "user_configs" / f"user_{user_id}.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuração não encontrada para o usuário {user_id}")
            return {}
            
    def format_message(self, insights: str, user_config: Dict[str, Any]) -> str:
        """Format the message according to user preferences."""
        if user_config.get("formato_preferido") == "resumo_executivo":
            # Add emojis and formatting for executive summary
            return f"📊 *Resumo Executivo*\n\n{insights}"
        elif user_config.get("formato_preferido") == "detalhado":
            # Add sections and formatting for detailed report
            return f"📈 *Relatório Detalhado*\n\n{insights}"
        else:
            # Default format
            return insights
            
    async def send_message(self, user_id: str, message: str) -> bool:
        """Send message via Telegram."""
        try:
            await self.telegram_api.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            return True
        except TelegramError as e:
            print(f"Erro ao enviar mensagem para {user_id}: {str(e)}")
            return False
            
    def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the Telegram dispatch task."""
        try:
            user_id = task_input.get("user_id")
            insights = task_input.get("insights")
            
            if not user_id or not insights:
                return {"status": "error", "message": "ID do usuário e insights são obrigatórios"}
                
            # Load user configuration
            user_config = self.load_user_config(user_id)
            if not user_config:
                return {"status": "error", "message": f"Configuração não encontrada para o usuário {user_id}"}
                
            # Format message according to user preferences
            formatted_message = self.format_message(insights, user_config)
            
            # Send message
            success = asyncio.run(self.send_message(user_id, formatted_message))
            
            if success:
                return {"status": "success", "message": f"Mensagem enviada com sucesso para {user_id}"}
            else:
                return {"status": "error", "message": f"Falha ao enviar mensagem para {user_id}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)} 