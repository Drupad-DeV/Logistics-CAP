"""
ETL Pipeline Orchestrator
Coordinates the entire data pipeline
"""
import pandas as pd
import yaml
import os
from typing import Dict, Optional
import logging

from .data_ingestion import DataIngestion
from .data_cleaning import DataCleaner
from .data_validation import DataValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Orchestrates the ETL pipeline"""
    
    def __init__(self, config_path: str):
        """
        Initialize ETL pipeline
        
        Args:
            config_path: Path to configuration file
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.ingestion = DataIngestion(self.config['data_sources']['raw_data_path'])
        self.cleaner = DataCleaner()
        self.validator = DataValidator(
            required_columns=self.config.get('validation_rules', {}).get('required_columns', [])
        )
        
    def run_pipeline(self, input_filename: str, output_filename: str) -> pd.DataFrame:
        """
        Run the complete ETL pipeline
        
        Args:
            input_filename: Name of input CSV file
            output_filename: Name of output CSV file
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("=" * 50)
        logger.info("Starting ETL Pipeline")
        logger.info("=" * 50)
        
        # Extract
        logger.info("Step 1: Data Ingestion")
        df = self.ingestion.load_csv(input_filename)
        data_info = self.ingestion.get_data_info(df)
        logger.info(f"Loaded data: {data_info['rows']} rows, {data_info['columns']} columns")
        
        # Validate initial data
        logger.info("\nStep 2: Initial Data Validation")
        validation_results = self.validator.validate_schema(df)
        quality_metrics = self.validator.check_data_quality(df)
        logger.info(f"Data quality: {quality_metrics['missing_percentage']:.2f}% missing values")
        
        # Transform
        logger.info("\nStep 3: Data Cleaning")
        
        # Remove duplicates
        if self.config['cleaning_rules'].get('remove_duplicates', False):
            df = self.cleaner.remove_duplicates(df)
        
        # Handle missing values
        if self.config['cleaning_rules'].get('handle_missing_values', False):
            strategy = self.config['cleaning_rules'].get('missing_value_strategy', 'drop')
            df = self.cleaner.handle_missing_values(df, strategy=strategy)
        
        # Convert data types if specified
        if 'data_types' in self.config.get('validation_rules', {}):
            type_mapping = {}
            for col, dtype in self.config['validation_rules']['data_types'].items():
                if col in df.columns:
                    if dtype == 'integer':
                        type_mapping[col] = 'int64'
                    elif dtype == 'float':
                        type_mapping[col] = 'float64'
            if type_mapping:
                df = self.cleaner.convert_data_types(df, type_mapping)
        
        # Final validation
        logger.info("\nStep 4: Final Data Validation")
        final_quality = self.validator.check_data_quality(df)
        logger.info(f"Final data quality: {final_quality['missing_percentage']:.2f}% missing values")
        logger.info(f"Final data size: {final_quality['total_rows']} rows, {final_quality['total_columns']} columns")
        
        # Load
        logger.info("\nStep 5: Saving Cleaned Data")
        output_path = os.path.join(
            self.config['data_sources']['cleaned_data_path'],
            output_filename
        )
        df.to_csv(output_path, index=False)
        logger.info(f"Saved cleaned data to {output_path}")
        
        logger.info("=" * 50)
        logger.info("ETL Pipeline Completed Successfully")
        logger.info("=" * 50)
        
        return df
    
    def get_pipeline_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get summary of pipeline results
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Dictionary with summary information
        """
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'summary_statistics': df.describe().to_dict()
        }
