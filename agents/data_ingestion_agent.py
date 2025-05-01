from typing import Dict, Any
import pandas as pd
from pathlib import Path
from crewai import Agent
from pydantic import BaseModel

class DataSource(BaseModel):
    """Model for data source configuration."""
    type: str  # csv, xlsx, json, sql
    path: str
    connection_string: str = None  # Only for SQL sources

class DataIngestionAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Data Ingestion Specialist",
            goal="Coletar e processar dados de vendas de múltiplas fontes",
            backstory="""Você é um especialista em ingestão de dados com experiência em 
            processamento de dados de vendas de diferentes fontes e formatos."""
        )
        self.data_dir = Path("data")
        
    def load_data(self, source: DataSource) -> pd.DataFrame:
        """Load data from the specified source."""
        try:
            if source.type == "csv":
                return pd.read_csv(source.path)
            elif source.type == "xlsx":
                return pd.read_excel(source.path)
            elif source.type == "json":
                return pd.read_json(source.path)
            elif source.type == "sql":
                if not source.connection_string:
                    raise ValueError("Connection string required for SQL sources")
                return pd.read_sql("SELECT * FROM sales", source.connection_string)
            else:
                raise ValueError(f"Unsupported data source type: {source.type}")
        except Exception as e:
            print(f"Error loading data from {source.path}: {str(e)}")
            raise
    
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the loaded data."""
        # Convert date columns to datetime
        date_columns = df.select_dtypes(include=['object']).columns[df.select_dtypes(include=['object']).apply(lambda x: x.str.contains(r'\d{4}-\d{2}-\d{2}').any())]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col])
            
        # Handle missing values
        df = df.fillna(method='ffill')
        
        # Ensure numeric columns are properly typed
        numeric_columns = df.select_dtypes(include=['object']).columns[df.select_dtypes(include=['object']).apply(lambda x: x.str.replace('.', '').str.isnumeric().all())]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col])
            
        return df
    
    def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the data ingestion task."""
        try:
            # Load data from all configured sources
            data_sources = task_input.get("data_sources", [])
            dfs = []
            
            for source_config in data_sources:
                source = DataSource(**source_config)
                df = self.load_data(source)
                df = self.process_data(df)
                dfs.append(df)
            
            # Combine all dataframes
            if dfs:
                combined_df = pd.concat(dfs, ignore_index=True)
                return {"status": "success", "data": combined_df}
            else:
                return {"status": "error", "message": "No data sources configured"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)} 