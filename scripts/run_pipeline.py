"""
Main script to run the ETL pipeline
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline.etl_pipeline import ETLPipeline
import argparse


def main():
    """Main function to run the pipeline"""
    parser = argparse.ArgumentParser(description='Run ETL Pipeline for Logistics Data')
    parser.add_argument('--input', '-i', required=True, help='Input CSV filename')
    parser.add_argument('--output', '-o', required=True, help='Output CSV filename')
    parser.add_argument('--config', '-c', 
                       default='config/pipeline_config.yaml',
                       help='Path to config file')
    
    args = parser.parse_args()
    
    # Initialize and run pipeline
    pipeline = ETLPipeline(args.config)
    df_cleaned = pipeline.run_pipeline(args.input, args.output)
    
    # Print summary
    print("\n" + "=" * 50)
    print("Pipeline Summary")
    print("=" * 50)
    summary = pipeline.get_pipeline_summary(df_cleaned)
    print(f"Total Rows: {summary['rows']}")
    print(f"Total Columns: {summary['columns']}")
    print(f"Columns: {', '.join(summary['column_names'])}")
    print("\nMissing Values:")
    for col, count in summary['missing_values'].items():
        if count > 0:
            print(f"  {col}: {count}")
    

if __name__ == '__main__':
    main()
