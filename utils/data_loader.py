from typing import Dict, List, Any
import json
from pathlib import Path
import pandas as pd
import jsonschema
from dotenv import load_dotenv
import os

def load_user_configs(config_dir: Path) -> List[Dict[str, Any]]:
    """Load all user configurations from the config directory."""
    try:
        # Load schema
        schema_path = config_dir / "rules_schema.json"
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
            
        # Load user configs
        user_configs = []
        user_configs_dir = config_dir / "user_configs"
        
        for config_file in user_configs_dir.glob("user_*.json"):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
                # Validate against schema
                jsonschema.validate(instance=config, schema=schema)
                user_configs.append(config)
                
        return user_configs
        
    except Exception as e:
        print(f"Error loading user configurations: {str(e)}")
        return []
        
def load_data_file(file_path: str) -> pd.DataFrame:
    """Load data from a file based on its extension."""
    try:
        file_path = Path(file_path)
        
        if file_path.suffix == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix == '.xlsx':
            return pd.read_excel(file_path)
        elif file_path.suffix == '.json':
            return pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
    except Exception as e:
        print(f"Error loading data file {file_path}: {str(e)}")
        raise
        
def load_database_data(connection_string: str, query: str) -> pd.DataFrame:
    """Load data from a database using the provided connection string and query."""
    try:
        return pd.read_sql(query, connection_string)
    except Exception as e:
        print(f"Error loading data from database: {str(e)}")
        raise
        
def load_environment_variables() -> Dict[str, str]:
    """Load environment variables from .env file."""
    try:
        load_dotenv()
        return {
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
            "DB_CONNECTION_STRING": os.getenv("DB_CONNECTION_STRING")
        }
    except Exception as e:
        print(f"Error loading environment variables: {str(e)}")
        return {} 