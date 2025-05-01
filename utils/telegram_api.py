from typing import Dict, Any
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv
import os

class TelegramAPI:
    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        self.bot = Bot(token=self.bot_token)
        
    async def send_message(self, chat_id: str, text: str, parse_mode: str = None) -> bool:
        """Send a message via Telegram."""
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode
            )
            return True
        except TelegramError as e:
            print(f"Error sending Telegram message: {str(e)}")
            return False
            
    async def send_document(self, chat_id: str, document_path: str, caption: str = None) -> bool:
        """Send a document via Telegram."""
        try:
            with open(document_path, 'rb') as doc:
                await self.bot.send_document(
                    chat_id=chat_id,
                    document=doc,
                    caption=caption
                )
            return True
        except TelegramError as e:
            print(f"Error sending Telegram document: {str(e)}")
            return False
            
    def send_message_sync(self, chat_id: str, text: str, parse_mode: str = None) -> bool:
        """Synchronous wrapper for send_message."""
        return asyncio.run(self.send_message(chat_id, text, parse_mode))
        
    def send_document_sync(self, chat_id: str, document_path: str, caption: str = None) -> bool:
        """Synchronous wrapper for send_document."""
        return asyncio.run(self.send_document(chat_id, document_path, caption))
        
    async def get_chat_info(self, chat_id: str) -> Dict[str, Any]:
        """Get information about a chat."""
        try:
            chat = await self.bot.get_chat(chat_id)
            return {
                "id": chat.id,
                "type": chat.type,
                "title": chat.title,
                "username": chat.username,
                "first_name": chat.first_name,
                "last_name": chat.last_name
            }
        except TelegramError as e:
            print(f"Error getting chat info: {str(e)}")
            return {}
            
    def get_chat_info_sync(self, chat_id: str) -> Dict[str, Any]:
        """Synchronous wrapper for get_chat_info."""
        return asyncio.run(self.get_chat_info(chat_id)) 