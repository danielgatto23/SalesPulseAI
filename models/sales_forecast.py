from typing import Dict, List, Optional
import pandas as pd
from prophet import Prophet
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
import numpy as np
import logging

class SalesForecastModel:
    def __init__(self, config: Dict):
        self.config = config
        self.prophet_model = None
        self.xgb_model = None
        self.scaler = StandardScaler()
        self.logger = logging.getLogger(__name__)

    def prepare_data(self, df: pd.DataFrame, persona_config: Dict) -> pd.DataFrame:
        """Prepara os dados de acordo com as configurações da persona."""
        try:
            # Seleciona métricas e segmentos baseado na configuração
            metrics = persona_config['previsao_vendas']['metricas']
            segments = persona_config['previsao_vendas']['segmentos']
            
            # Agrupa dados pelos segmentos selecionados
            if 'geral' not in segments:
                group_cols = [col for col in segments if col in df.columns]
                if group_cols:
                    df = df.groupby(['date'] + group_cols)[metrics].sum().reset_index()
            
            return df
        except Exception as e:
            self.logger.error(f"Erro ao preparar dados: {str(e)}")
            raise

    def train_prophet(self, df: pd.DataFrame, persona_config: Dict) -> None:
        """Treina modelo Prophet com configurações específicas da persona."""
        try:
            horizon = persona_config['previsao_vendas']['horizonte']
            self.prophet_model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                changepoint_prior_scale=0.05
            )
            
            # Ajusta sazonalidade baseado no nível de detalhe
            if persona_config['previsao_vendas']['nivel_detalhe'] == 'muito_alto':
                self.prophet_model.add_seasonality(
                    name='monthly',
                    period=30.5,
                    fourier_order=5
                )
            
            self.prophet_model.fit(df)
        except Exception as e:
            self.logger.error(f"Erro ao treinar Prophet: {str(e)}")
            raise

    def train_xgboost(self, df: pd.DataFrame, persona_config: Dict) -> None:
        """Treina modelo XGBoost com configurações específicas da persona."""
        try:
            # Prepara features baseado no nível de detalhe
            features = self._prepare_features(df, persona_config)
            target = df['y'].values
            
            # Escala features
            features_scaled = self.scaler.fit_transform(features)
            
            # Configura modelo baseado no nível de detalhe
            if persona_config['previsao_vendas']['nivel_detalhe'] == 'muito_alto':
                params = {
                    'max_depth': 6,
                    'learning_rate': 0.1,
                    'n_estimators': 200
                }
            else:
                params = {
                    'max_depth': 4,
                    'learning_rate': 0.1,
                    'n_estimators': 100
                }
            
            self.xgb_model = xgb.XGBRegressor(**params)
            self.xgb_model.fit(features_scaled, target)
        except Exception as e:
            self.logger.error(f"Erro ao treinar XGBoost: {str(e)}")
            raise

    def _prepare_features(self, df: pd.DataFrame, persona_config: Dict) -> pd.DataFrame:
        """Prepara features para XGBoost baseado nas configurações."""
        features = pd.DataFrame()
        
        # Adiciona features temporais
        df['date'] = pd.to_datetime(df['date'])
        features['day_of_week'] = df['date'].dt.dayofweek
        features['month'] = df['date'].dt.month
        
        if persona_config['previsao_vendas']['nivel_detalhe'] in ['alto', 'muito_alto']:
            features['day_of_month'] = df['date'].dt.day
            features['quarter'] = df['date'].dt.quarter
        
        # Adiciona métricas como features
        for metric in persona_config['previsao_vendas']['metricas']:
            if metric in df.columns:
                features[f'lag1_{metric}'] = df[metric].shift(1)
                features[f'lag7_{metric}'] = df[metric].shift(7)
                
                if persona_config['previsao_vendas']['nivel_detalhe'] == 'muito_alto':
                    features[f'lag30_{metric}'] = df[metric].shift(30)
                    features[f'rolling_mean_7_{metric}'] = df[metric].rolling(7).mean()
        
        return features.fillna(0)

    def generate_forecast(self, df: pd.DataFrame, persona_config: Dict) -> pd.DataFrame:
        """Gera previsões usando o método especificado na configuração da persona."""
        try:
            method = persona_config['previsao_vendas']['metodo']
            horizon = persona_config['previsao_vendas']['horizonte']
            
            if method == 'prophet':
                return self._generate_prophet_forecast(df, horizon)
            elif method == 'xgb':
                return self._generate_xgb_forecast(df, horizon)
            else:
                raise ValueError(f"Método de previsão inválido: {method}")
        except Exception as e:
            self.logger.error(f"Erro ao gerar previsão: {str(e)}")
            raise

    def _generate_prophet_forecast(self, df: pd.DataFrame, horizon: int) -> pd.DataFrame:
        """Gera previsão usando Prophet."""
        future = self.prophet_model.make_future_dataframe(periods=horizon)
        forecast = self.prophet_model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    def _generate_xgb_forecast(self, df: pd.DataFrame, horizon: int) -> pd.DataFrame:
        """Gera previsão usando XGBoost."""
        features = self._prepare_features(df, self.config)
        features_scaled = self.scaler.transform(features)
        
        predictions = []
        last_date = df['date'].max()
        
        for i in range(horizon):
            pred = self.xgb_model.predict(features_scaled[-1:])
            predictions.append(pred[0])
            
            # Atualiza features para próxima previsão
            new_features = self._update_features(features, pred[0])
            features_scaled = self.scaler.transform(new_features)
        
        forecast_dates = pd.date_range(start=last_date, periods=horizon+1, freq='D')[1:]
        return pd.DataFrame({
            'ds': forecast_dates,
            'yhat': predictions,
            'yhat_lower': [p * 0.9 for p in predictions],
            'yhat_upper': [p * 1.1 for p in predictions]
        })

    def _update_features(self, features: pd.DataFrame, new_value: float) -> pd.DataFrame:
        """Atualiza features para próxima previsão."""
        new_features = features.copy()
        new_features.iloc[-1] = new_features.iloc[-2]
        new_features.iloc[-1, 0] = new_value
        return new_features 