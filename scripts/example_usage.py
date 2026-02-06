"""
Example: Using the Pipeline Programmatically
This script demonstrates how to use the pipeline components in your own code
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline.data_ingestion import DataIngestion
from pipeline.data_cleaning import DataCleaner
from pipeline.data_validation import DataValidator
import pandas as pd


def example_basic_usage():
    """Example 1: Basic pipeline usage"""
    print("=" * 60)
    print("Example 1: Basic Pipeline Usage")
    print("=" * 60)
    
    # Load data
    ingestion = DataIngestion('data/raw')
    df = ingestion.load_csv('logistics_data.csv')
    print(f"\n1. Loaded {len(df)} rows")
    
    # Clean data
    cleaner = DataCleaner()
    df = cleaner.remove_duplicates(df)
    df = cleaner.handle_missing_values(df, strategy='fill')
    print(f"2. Cleaned data now has {len(df)} rows")
    
    # Validate data
    validator = DataValidator()
    quality = validator.check_data_quality(df)
    print(f"3. Data quality: {quality['missing_percentage']:.2f}% missing")
    print(f"4. Duplicate rows: {quality['duplicate_rows']}")
    
    print("\n✓ Basic usage complete!\n")
    return df


def example_custom_cleaning():
    """Example 2: Custom cleaning operations"""
    print("=" * 60)
    print("Example 2: Custom Cleaning Operations")
    print("=" * 60)
    
    # Load data
    ingestion = DataIngestion('data/raw')
    df = ingestion.load_csv('logistics_data.csv')
    
    # Custom cleaning
    cleaner = DataCleaner()
    
    # Standardize text columns
    df = cleaner.standardize_text(df, ['origin', 'destination', 'status', 'carrier'])
    print("\n1. Standardized text columns")
    
    # Convert data types
    type_mapping = {
        'shipment_date': 'datetime',
        'delivery_date': 'datetime'
    }
    df = cleaner.convert_data_types(df, type_mapping)
    print("2. Converted date columns to datetime")
    
    # Display sample
    print("\n3. Sample of cleaned data:")
    print(df[['shipment_id', 'origin', 'destination', 'status']].head(3))
    
    print("\n✓ Custom cleaning complete!\n")
    return df


def example_validation():
    """Example 3: Data validation"""
    print("=" * 60)
    print("Example 3: Data Validation")
    print("=" * 60)
    
    # Load data
    ingestion = DataIngestion('data/raw')
    df = ingestion.load_csv('logistics_data.csv')
    
    # Validate schema
    required_cols = ['shipment_id', 'origin', 'destination', 'shipment_date']
    validator = DataValidator(required_columns=required_cols)
    
    schema_results = validator.validate_schema(df)
    print(f"\n1. Has required columns: {schema_results['has_required_columns']}")
    
    # Validate data types
    expected_types = {
        'shipment_id': 'string',
        'quantity': 'integer',
        'weight': 'float',
        'cost': 'float'
    }
    type_results = validator.validate_data_types(df, expected_types)
    print(f"2. Data type validation results:")
    for col, valid in type_results.items():
        status = "✓" if valid else "✗"
        print(f"   {status} {col}: {'Valid' if valid else 'Invalid'}")
    
    # Quality metrics
    quality = validator.check_data_quality(df)
    print(f"\n3. Quality Metrics:")
    print(f"   - Total rows: {quality['total_rows']}")
    print(f"   - Missing cells: {quality['missing_cells']}")
    print(f"   - Missing %: {quality['missing_percentage']:.2f}%")
    print(f"   - Duplicates: {quality['duplicate_rows']}")
    
    print("\n✓ Validation complete!\n")


def example_full_pipeline():
    """Example 4: Using the full ETL pipeline"""
    print("=" * 60)
    print("Example 4: Full ETL Pipeline")
    print("=" * 60)
    
    from pipeline.etl_pipeline import ETLPipeline
    
    # Initialize and run pipeline
    pipeline = ETLPipeline('config/pipeline_config.yaml')
    df = pipeline.run_pipeline('logistics_data.csv', 'example_cleaned.csv')
    
    # Get summary
    summary = pipeline.get_pipeline_summary(df)
    print(f"\n✓ Pipeline Summary:")
    print(f"   - Processed {summary['rows']} rows")
    print(f"   - Output has {summary['columns']} columns")
    print(f"   - Columns: {', '.join(summary['column_names'])}")
    
    print("\n✓ Full pipeline complete!\n")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Logistics Data Pipeline - Examples")
    print("=" * 60 + "\n")
    
    # Run all examples
    example_basic_usage()
    example_custom_cleaning()
    example_validation()
    example_full_pipeline()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
