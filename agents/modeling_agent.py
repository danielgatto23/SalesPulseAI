from typing import Dict, Any, List
import pandas as pd
import numpy as np
from prophet import Prophet
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from crewai import Agent
from models.sales_forecasting import SalesForecastingModel
from models.product_recommendation import ProductRecommendationModel

class ModelingAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Data Scientist",
            goal="Gerar previsões de vendas e recomendações de produtos",
            backstory="""Você é um cientista de dados especializado em previsão de vendas 
            e sistemas de recomendação, com experiência em múltiplos algoritmos."""
        )
        self.forecasting_model = SalesForecastingModel()
        self.recommendation_model = ProductRecommendationModel()
        
    def prepare_forecasting_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for forecasting."""
        # Ensure we have the required columns
        required_columns = ['date', 'sales']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("DataFrame must contain 'date' and 'sales' columns")
            
        # Prepare data for Prophet
        prophet_df = df[['date', 'sales']].copy()
        prophet_df.columns = ['ds', 'y']
        return prophet_df
    
    def prepare_recommendation_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for product recommendations."""
        # Ensure we have the required columns
        required_columns = ['user_id', 'product_id', 'rating']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("DataFrame must contain 'user_id', 'product_id', and 'rating' columns")
            
        return df[required_columns]
    
    def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the modeling task."""
        try:
            data = task_input.get("data")
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Input data must be a pandas DataFrame")
                
            # Prepare data
            forecasting_data = self.prepare_forecasting_data(data)
            recommendation_data = self.prepare_recommendation_data(data)
            
            # Generate forecasts
            prophet_forecast = self.forecasting_model.predict_with_prophet(forecasting_data)
            xgboost_forecast = self.forecasting_model.predict_with_xgboost(forecasting_data)
            
            # Generate recommendations
            recommendations = self.recommendation_model.generate_recommendations(recommendation_data)
            
            return {
                "status": "success",
                "forecasts": {
                    "prophet": prophet_forecast,
                    "xgboost": xgboost_forecast
                },
                "recommendations": recommendations
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)} 