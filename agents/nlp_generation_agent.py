from typing import Dict, Any
import google.generativeai as genai
from pathlib import Path
from crewai import Agent
import json

class NLPGenerationAgent(Agent):
    def __init__(self):
        super().__init__(
            role="NLP Specialist",
            goal="Gerar insights em linguagem natural a partir dos dados analisados",
            backstory="""Você é um especialista em processamento de linguagem natural, 
            com experiência em geração de insights e relatórios em linguagem natural."""
        )
        self.templates_dir = Path("templates")
        self.api_key = self._load_api_key()
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def _load_api_key(self) -> str:
        """Load the Gemini API key from environment variables."""
        try:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            return os.getenv("GEMINI_API_KEY")
        except Exception as e:
            print(f"Error loading API key: {str(e)}")
            raise
            
    def load_template(self, persona: str) -> str:
        """Load the template for the specified persona."""
        template_path = self.templates_dir / f"{persona}.txt"
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Template not found for persona: {persona}")
            return ""
            
    def generate_insights(self, data: Dict[str, Any], persona: str) -> str:
        """Generate insights using the Gemini model."""
        template = self.load_template(persona)
        if not template:
            return "Template não encontrado para a persona especificada."
            
        # Prepare the prompt
        prompt = f"""
        Com base nos dados fornecidos e no template abaixo, gere um relatório de insights em português.
        
        Template:
        {template}
        
        Dados:
        {json.dumps(data, indent=2)}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return f"Erro ao gerar insights: {str(e)}"
            
    def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the NLP generation task."""
        try:
            data = task_input.get("data")
            persona = task_input.get("persona")
            
            if not data or not persona:
                return {"status": "error", "message": "Dados e persona são obrigatórios"}
                
            insights = self.generate_insights(data, persona)
            
            return {
                "status": "success",
                "insights": insights
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)} 