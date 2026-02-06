"""
Data Ingestion Module
Handles loading raw CSV data files
"""
import pandas as pd
import os
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataIngestion:
    """Handles data ingestion from CSV files"""
    
    def __init__(self, raw_data_path: str):
        """
        Initialize data ingestion
        
        Args:
            raw_data_path: Path to raw data directory
        """
        self.raw_data_path = raw_data_path
        
    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Load a CSV file into a pandas DataFrame
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            DataFrame containing the data
        """
        filepath = os.path.join(self.raw_data_path, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        
        return df
    
    def load_multiple_csv(self, filenames: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Load multiple CSV files
        
        Args:
            filenames: List of CSV filenames
            
        Returns:
            Dictionary mapping filename to DataFrame
        """
        data = {}
        for filename in filenames:
            try:
                data[filename] = self.load_csv(filename)
            except Exception as e:
                logger.error(f"Error loading {filename}: {str(e)}")
                
        return data
    
    def get_data_info(self, df: pd.DataFrame) -> Dict:
        """
        Get information about the DataFrame
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with data information
        """
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
