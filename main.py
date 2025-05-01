import os
import json
from datetime import datetime
from typing import Dict, List
from pathlib import Path

from crewai import Agent, Task, Crew, Process
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from agents.data_ingestion_agent import DataIngestionAgent
from agents.modeling_agent import ModelingAgent
from agents.nlp_generation_agent import NLPGenerationAgent
from agents.telegram_dispatch_agent import TelegramDispatchAgent
from utils.data_loader import load_user_configs
from utils.telegram_api import TelegramAPI

class SalesInsightsSystem:
    def __init__(self):
        self.config_dir = Path("config")
        self.user_configs = load_user_configs(self.config_dir / "user_configs")
        self.telegram_api = TelegramAPI()
        self.scheduler = BackgroundScheduler()
        
        # Initialize agents
        self.data_ingestion_agent = DataIngestionAgent()
        self.modeling_agent = ModelingAgent()
        self.nlp_generation_agent = NLPGenerationAgent()
        self.telegram_dispatch_agent = TelegramDispatchAgent(self.telegram_api)
        
    def create_crew(self, user_config: Dict) -> Crew:
        """Create a CrewAI crew for processing a single user's insights."""
        tasks = [
            Task(
                description=f"Coletar e processar dados de vendas para {user_config['persona']}",
                agent=self.data_ingestion_agent
            ),
            Task(
                description=f"Gerar previsões e recomendações para {user_config['persona']}",
                agent=self.modeling_agent
            ),
            Task(
                description=f"Gerar insights em linguagem natural para {user_config['persona']}",
                agent=self.nlp_generation_agent
            ),
            Task(
                description=f"Enviar insights via Telegram para {user_config['usuario_id']}",
                agent=self.telegram_dispatch_agent
            )
        ]
        
        return Crew(
            agents=[self.data_ingestion_agent, self.modeling_agent, 
                   self.nlp_generation_agent, self.telegram_dispatch_agent],
            tasks=tasks,
            process=Process.sequential
        )
    
    def process_user_insights(self, user_config: Dict):
        """Process insights for a single user."""
        try:
            crew = self.create_crew(user_config)
            crew.kickoff()
            print(f"Processamento concluído para usuário {user_config['usuario_id']}")
        except Exception as e:
            print(f"Erro ao processar insights para usuário {user_config['usuario_id']}: {str(e)}")
    
    def schedule_jobs(self):
        """Schedule jobs for all users based on their preferences."""
        for user_config in self.user_configs:
            # Parse the preferred time
            hour, minute = map(int, user_config['horario_preferido'].split(':'))
            
            # Schedule based on frequency
            if user_config['frequencia_envio'] == 'diario':
                self.scheduler.add_job(
                    self.process_user_insights,
                    CronTrigger(hour=hour, minute=minute),
                    args=[user_config],
                    id=f"user_{user_config['usuario_id']}"
                )
            elif user_config['frequencia_envio'] == 'semanal':
                self.scheduler.add_job(
                    self.process_user_insights,
                    CronTrigger(day_of_week='mon', hour=hour, minute=minute),
                    args=[user_config],
                    id=f"user_{user_config['usuario_id']}"
                )
    
    def start(self):
        """Start the system."""
        self.schedule_jobs()
        self.scheduler.start()
        print("Sistema de Insights de Vendas iniciado!")
        
    def stop(self):
        """Stop the system."""
        self.scheduler.shutdown()
        print("Sistema de Insights de Vendas encerrado.")

if __name__ == "__main__":
    system = SalesInsightsSystem()
    try:
        system.start()
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        system.stop() 