# Quick Start Guide

This guide will help you get started with the Logistics Data Engineering Pipeline.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Drupad-DeV/Logistics-CAP.git
cd Logistics-CAP
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start Examples

### Example 1: Check Data Quality

Before processing your data, check its quality:

```bash
python scripts/check_data_quality.py --file logistics_data.csv
```

### Example 2: Run the ETL Pipeline

Process your data through the complete pipeline:

```bash
python scripts/run_pipeline.py --input logistics_data.csv --output cleaned_logistics.csv
```

The pipeline will:
1. Load the data from `data/raw/logistics_data.csv`
2. Remove duplicates
3. Handle missing values
4. Validate data quality
5. Save cleaned data to `data/cleaned/cleaned_logistics.csv`

### Example 3: Using the Pipeline in Your Code

You can also use the pipeline components in your own Python scripts:

```python
import sys
sys.path.insert(0, 'src')

from pipeline.etl_pipeline import ETLPipeline

# Initialize pipeline
pipeline = ETLPipeline('config/pipeline_config.yaml')

# Run pipeline
cleaned_df = pipeline.run_pipeline('logistics_data.csv', 'my_cleaned_data.csv')

# Get summary
summary = pipeline.get_pipeline_summary(cleaned_df)
print(f"Cleaned {summary['rows']} rows with {summary['columns']} columns")
```

## Running Tests

To verify the installation and functionality:

```bash
python -m unittest tests.test_pipeline -v
```

## Support

For issues or questions, check the main README.md or open an issue on GitHub.
