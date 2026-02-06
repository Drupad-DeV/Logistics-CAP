"""
Data Quality Check Script
Performs data quality checks on CSV files
"""
import sys
import os
import pandas as pd

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline.data_validation import DataValidator
import argparse


def main():
    """Main function to check data quality"""
    parser = argparse.ArgumentParser(description='Check Data Quality')
    parser.add_argument('--file', '-f', required=True, help='CSV file to check')
    parser.add_argument('--dir', '-d', default='data/raw', help='Directory containing the file')
    
    args = parser.parse_args()
    
    # Load data
    filepath = os.path.join(args.dir, args.file)
    df = pd.read_csv(filepath)
    
    # Initialize validator
    validator = DataValidator()
    
    # Run quality checks
    print("\n" + "=" * 50)
    print("Data Quality Report")
    print("=" * 50)
    
    quality_metrics = validator.check_data_quality(df)
    
    print(f"\nDataset Information:")
    print(f"  Total Rows: {quality_metrics['total_rows']}")
    print(f"  Total Columns: {quality_metrics['total_columns']}")
    print(f"  Total Cells: {quality_metrics['total_cells']}")
    
    print(f"\nData Quality Metrics:")
    print(f"  Missing Cells: {quality_metrics['missing_cells']}")
    print(f"  Missing Percentage: {quality_metrics['missing_percentage']:.2f}%")
    print(f"  Duplicate Rows: {quality_metrics['duplicate_rows']}")
    
    if quality_metrics['columns_with_missing']:
        print(f"\nColumns with Missing Values:")
        for col in quality_metrics['columns_with_missing']:
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / len(df)) * 100
            print(f"  {col}: {missing_count} ({missing_pct:.2f}%)")
    
    print("\nData Types:")
    for col, dtype in df.dtypes.items():
        print(f"  {col}: {dtype}")
    
    print("\n" + "=" * 50)
    

if __name__ == '__main__':
    main()
