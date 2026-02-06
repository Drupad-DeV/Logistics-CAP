"""
Data Cleaning Module
Handles cleaning and preprocessing of data
"""
import pandas as pd
import numpy as np
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCleaner:
    """Handles data cleaning operations"""
    
    def __init__(self):
        """Initialize data cleaner"""
        pass
    
    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows
        
        Args:
            df: Input DataFrame
            subset: Columns to check for duplicates
            
        Returns:
            DataFrame with duplicates removed
        """
        initial_rows = len(df)
        df_clean = df.drop_duplicates(subset=subset, keep='first')
        removed_rows = initial_rows - len(df_clean)
        
        logger.info(f"Removed {removed_rows} duplicate rows")
        return df_clean
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'drop', 
                            fill_value: Optional[dict] = None) -> pd.DataFrame:
        """
        Handle missing values in DataFrame
        
        Args:
            df: Input DataFrame
            strategy: Strategy to handle missing values ('drop', 'fill', 'interpolate')
            fill_value: Dictionary mapping column names to fill values
            
        Returns:
            DataFrame with missing values handled
        """
        df_clean = df.copy()
        
        if strategy == 'drop':
            initial_rows = len(df_clean)
            df_clean = df_clean.dropna()
            logger.info(f"Dropped {initial_rows - len(df_clean)} rows with missing values")
            
        elif strategy == 'fill':
            if fill_value:
                df_clean = df_clean.fillna(fill_value)
            else:
                # Fill numeric columns with mean, categorical with mode
                for col in df_clean.columns:
                    if df_clean[col].dtype in ['int64', 'float64']:
                        df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
                    else:
                        df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown')
            logger.info("Filled missing values")
            
        elif strategy == 'interpolate':
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            df_clean[numeric_cols] = df_clean[numeric_cols].interpolate()
            logger.info("Interpolated missing values in numeric columns")
            
        return df_clean
    
    def standardize_text(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Standardize text columns (lowercase, strip whitespace)
        
        Args:
            df: Input DataFrame
            columns: List of columns to standardize
            
        Returns:
            DataFrame with standardized text
        """
        df_clean = df.copy()
        
        for col in columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()
                
        logger.info(f"Standardized text in columns: {columns}")
        return df_clean
    
    def convert_data_types(self, df: pd.DataFrame, type_mapping: dict) -> pd.DataFrame:
        """
        Convert column data types
        
        Args:
            df: Input DataFrame
            type_mapping: Dictionary mapping column names to data types
            
        Returns:
            DataFrame with converted data types
        """
        df_clean = df.copy()
        
        for col, dtype in type_mapping.items():
            if col in df_clean.columns:
                try:
                    if dtype == 'datetime':
                        df_clean[col] = pd.to_datetime(df_clean[col])
                    else:
                        df_clean[col] = df_clean[col].astype(dtype)
                    logger.info(f"Converted {col} to {dtype}")
                except Exception as e:
                    logger.error(f"Error converting {col} to {dtype}: {str(e)}")
                    
        return df_clean
    
    def remove_outliers(self, df: pd.DataFrame, column: str, method: str = 'iqr', 
                       threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers from a numeric column
        
        Args:
            df: Input DataFrame
            column: Column name
            method: Method to detect outliers ('iqr' or 'zscore')
            threshold: Threshold for outlier detection
            
        Returns:
            DataFrame with outliers removed
        """
        df_clean = df.copy()
        initial_rows = len(df_clean)
        
        if column not in df_clean.columns:
            logger.warning(f"Column {column} not found")
            return df_clean
            
        if method == 'iqr':
            Q1 = df_clean[column].quantile(0.25)
            Q3 = df_clean[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df_clean = df_clean[(df_clean[column] >= lower_bound) & (df_clean[column] <= upper_bound)]
            
        elif method == 'zscore':
            mean = df_clean[column].mean()
            std = df_clean[column].std()
            df_clean = df_clean[np.abs((df_clean[column] - mean) / std) <= threshold]
            
        removed_rows = initial_rows - len(df_clean)
        logger.info(f"Removed {removed_rows} outliers from {column}")
        
        return df_clean
