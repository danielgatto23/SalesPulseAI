from typing import Dict, Any
import pandas as pd
import numpy as np
from prophet import Prophet
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

class SalesForecastingModel:
    def __init__(self):
        self.prophet_model = None
        self.xgboost_model = None
        self.scaler = StandardScaler()
        
    def prepare_xgboost_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for XGBoost model."""
        # Create time-based features
        df['year'] = df['ds'].dt.year
        df['month'] = df['ds'].dt.month
        df['day'] = df['ds'].dt.day
        df['dayofweek'] = df['ds'].dt.dayofweek
        df['quarter'] = df['ds'].dt.quarter
        
        # Create lag features
        df['lag_7'] = df['y'].shift(7)
        df['lag_14'] = df['y'].shift(14)
        df['lag_30'] = df['y'].shift(30)
        
        # Create rolling features
        df['rolling_mean_7'] = df['y'].rolling(window=7).mean()
        df['rolling_std_7'] = df['y'].rolling(window=7).std()
        
        # Drop rows with NaN values
        df = df.dropna()
        
        return df
        
    def predict_with_prophet(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate forecast using Prophet."""
        try:
            # Initialize and fit the model
            self.prophet_model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=True
            )
            self.prophet_model.fit(df)
            
            # Create future dates for forecasting
            future = self.prophet_model.make_future_dataframe(periods=30)
            
            # Generate forecast
            forecast = self.prophet_model.predict(future)
            
            return {
                "forecast": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).to_dict('records'),
                "metrics": {
                    "mse": mean_squared_error(df['y'], forecast['yhat'][:len(df)])
                }
            }
            
        except Exception as e:
            print(f"Error in Prophet forecasting: {str(e)}")
            return {"error": str(e)}
            
    def predict_with_xgboost(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate forecast using XGBoost."""
        try:
            # Prepare features
            feature_df = self.prepare_xgboost_features(df)
            
            # Split into features and target
            X = feature_df.drop(['ds', 'y'], axis=1)
            y = feature_df['y']
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Initialize and fit the model
            self.xgboost_model = xgb.XGBRegressor(
                objective='reg:squarederror',
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6
            )
            self.xgboost_model.fit(X_scaled, y)
            
            # Generate future dates
            last_date = df['ds'].max()
            future_dates = pd.date_range(start=last_date, periods=31, freq='D')[1:]
            
            # Create future features
            future_df = pd.DataFrame({'ds': future_dates})
            future_features = self.prepare_xgboost_features(future_df)
            future_X = future_features.drop(['ds', 'y'], axis=1)
            future_X_scaled = self.scaler.transform(future_X)
            
            # Generate forecast
            forecast = self.xgboost_model.predict(future_X_scaled)
            
            return {
                "forecast": [
                    {
                        "ds": str(date),
                        "yhat": float(pred),
                        "yhat_lower": float(pred * 0.9),
                        "yhat_upper": float(pred * 1.1)
                    }
                    for date, pred in zip(future_dates, forecast)
                ],
                "metrics": {
                    "mse": mean_squared_error(y, self.xgboost_model.predict(X_scaled))
                }
            }
            
        except Exception as e:
            print(f"Error in XGBoost forecasting: {str(e)}")
            return {"error": str(e)} 