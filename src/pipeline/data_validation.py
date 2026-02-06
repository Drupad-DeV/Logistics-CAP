"""
Data Validation Module
Validates data quality and schema
"""
import pandas as pd
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    """Handles data validation"""
    
    def __init__(self, required_columns: Optional[List[str]] = None):
        """
        Initialize data validator
        
        Args:
            required_columns: List of required column names
        """
        self.required_columns = required_columns or []
        
    def validate_schema(self, df: pd.DataFrame) -> Dict[str, bool]:
        """
        Validate DataFrame schema
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with validation results
        """
        results = {}
        
        # Check required columns
        missing_columns = set(self.required_columns) - set(df.columns)
        results['has_required_columns'] = len(missing_columns) == 0
        results['missing_columns'] = list(missing_columns)
        
        # Check for empty DataFrame
        results['is_not_empty'] = len(df) > 0
        
        # Check for all null columns
        all_null_cols = [col for col in df.columns if df[col].isnull().all()]
        results['has_all_null_columns'] = len(all_null_cols) > 0
        results['all_null_columns'] = all_null_cols
        
        return results
    
    def validate_data_types(self, df: pd.DataFrame, expected_types: Dict[str, str]) -> Dict[str, bool]:
        """
        Validate column data types
        
        Args:
            df: Input DataFrame
            expected_types: Dictionary mapping column names to expected types
            
        Returns:
            Dictionary with validation results
        """
        results = {}
        
        for col, expected_type in expected_types.items():
            if col not in df.columns:
                results[col] = False
                continue
                
            actual_type = str(df[col].dtype)
            
            # Map expected types to pandas types
            type_mapping = {
                'string': ['object', 'string'],
                'integer': ['int64', 'int32', 'int16', 'int8'],
                'float': ['float64', 'float32'],
                'datetime': ['datetime64[ns]', 'datetime64'],
                'boolean': ['bool']
            }
            
            expected_dtypes = type_mapping.get(expected_type, [expected_type])
            results[col] = actual_type in expected_dtypes
            
        return results
    
    def check_data_quality(self, df: pd.DataFrame) -> Dict:
        """
        Check overall data quality
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with quality metrics
        """
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'total_cells': total_cells,
            'missing_cells': missing_cells,
            'missing_percentage': (missing_cells / total_cells * 100) if total_cells > 0 else 0,
            'duplicate_rows': df.duplicated().sum(),
            'columns_with_missing': list(df.columns[df.isnull().any()]),
        }
    
    def validate_value_ranges(self, df: pd.DataFrame, range_rules: Dict[str, tuple]) -> Dict[str, bool]:
        """
        Validate that values are within expected ranges
        
        Args:
            df: Input DataFrame
            range_rules: Dictionary mapping column names to (min, max) tuples
            
        Returns:
            Dictionary with validation results
        """
        results = {}
        
        for col, (min_val, max_val) in range_rules.items():
            if col not in df.columns:
                results[col] = False
                continue
                
            if df[col].dtype in ['int64', 'float64']:
                within_range = df[col].between(min_val, max_val, inclusive='both').all()
                results[col] = within_range
            else:
                results[col] = False
                
        return results
