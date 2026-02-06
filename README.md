# Logistics-CAP
Repository for Capstone Project LTIM Logistics

## Overview
This is a comprehensive Data Engineering project for logistics data processing. The project includes a complete ETL pipeline for CSV data with cleaning, validation, and transformation capabilities.

## Features
- **Data Ingestion**: Load and process CSV files from raw data sources
- **Data Cleaning**: Remove duplicates, handle missing values, standardize text, and remove outliers
- **Data Validation**: Schema validation, data type checking, and quality metrics
- **ETL Pipeline**: Complete orchestration of Extract-Transform-Load operations
- **Configurable**: YAML-based configuration for pipeline parameters

## Project Structure
```
Logistics-CAP/
├── config/                      # Configuration files
│   └── pipeline_config.yaml     # Pipeline configuration
├── data/                        # Data directories
│   ├── raw/                     # Raw input data
│   ├── processed/               # Intermediate processed data
│   └── cleaned/                 # Final cleaned data
├── src/                         # Source code
│   ├── pipeline/                # Pipeline modules
│   │   ├── data_ingestion.py   # Data loading
│   │   ├── data_cleaning.py    # Data cleaning operations
│   │   ├── data_validation.py  # Data validation
│   │   └── etl_pipeline.py     # ETL orchestration
│   └── utils/                   # Utility functions
│       └── helpers.py           # Helper functions
├── scripts/                     # Executable scripts
│   ├── run_pipeline.py          # Main pipeline runner
│   └── check_data_quality.py   # Data quality checker
├── tests/                       # Test files
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Drupad-DeV/Logistics-CAP.git
cd Logistics-CAP
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the ETL Pipeline

Run the complete pipeline on your data:

```bash
python scripts/run_pipeline.py --input logistics_data.csv --output cleaned_logistics.csv
```

Options:
- `--input`, `-i`: Input CSV filename (must be in data/raw/)
- `--output`, `-o`: Output CSV filename (will be saved in data/cleaned/)
- `--config`, `-c`: Path to config file (default: config/pipeline_config.yaml)

### Checking Data Quality

Check the quality of your raw data before processing:

```bash
python scripts/check_data_quality.py --file logistics_data.csv
```

Options:
- `--file`, `-f`: CSV filename to check
- `--dir`, `-d`: Directory containing the file (default: data/raw)

### Configuration

Edit `config/pipeline_config.yaml` to customize the pipeline behavior:

```yaml
cleaning_rules:
  remove_duplicates: true
  handle_missing_values: true
  missing_value_strategy: "fill"  # Options: fill, drop, interpolate
  
validation_rules:
  required_columns:
    - shipment_id
    - origin
    - destination
```

## Pipeline Stages

### 1. Data Ingestion
- Loads CSV files from the raw data directory
- Provides data information and statistics
- Supports loading multiple files

### 2. Data Cleaning
- **Remove Duplicates**: Identifies and removes duplicate rows
- **Handle Missing Values**: Fill, drop, or interpolate missing data
- **Standardize Text**: Lowercase and trim whitespace
- **Convert Data Types**: Ensure correct data types
- **Remove Outliers**: IQR or Z-score based outlier detection

### 3. Data Validation
- **Schema Validation**: Verify required columns exist
- **Data Type Validation**: Check column data types
- **Quality Metrics**: Calculate completeness and quality scores
- **Value Range Validation**: Ensure values are within expected ranges

### 4. Data Output
- Saves cleaned data to the cleaned directory
- Configurable output format and encoding

## Sample Data

The repository includes sample logistics data (`data/raw/logistics_data.csv`) with the following schema:

| Column | Type | Description |
|--------|------|-------------|
| shipment_id | string | Unique shipment identifier |
| origin | string | Origin city |
| destination | string | Destination city |
| shipment_date | date | Date of shipment |
| delivery_date | date | Date of delivery |
| quantity | integer | Quantity of items |
| weight | float | Weight in kg |
| cost | float | Cost in INR |
| status | string | Shipment status |
| carrier | string | Carrier name |

## Example Output

When running the pipeline, you'll see detailed logs:

```
==================================================
Starting ETL Pipeline
==================================================
Step 1: Data Ingestion
Loaded data: 11 rows, 10 columns

Step 2: Initial Data Validation
Data quality: 18.18% missing values

Step 3: Data Cleaning
Removed 1 duplicate rows
Filled missing values

Step 4: Final Data Validation
Final data quality: 0.00% missing values
Final data size: 10 rows, 10 columns

Step 5: Saving Cleaned Data
Saved cleaned data to data/cleaned/cleaned_logistics.csv
==================================================
ETL Pipeline Completed Successfully
==================================================
```

## Development

### Adding New Cleaning Rules

Extend the `DataCleaner` class in `src/pipeline/data_cleaning.py`:

```python
def custom_cleaning_method(self, df: pd.DataFrame) -> pd.DataFrame:
    # Your cleaning logic here
    return df
```

### Adding New Validation Rules

Extend the `DataValidator` class in `src/pipeline/data_validation.py`:

```python
def validate_custom_rule(self, df: pd.DataFrame) -> Dict:
    # Your validation logic here
    return results
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Drupad Dev P

## Acknowledgments

- LTIM for the Capstone Project opportunity
- Logistics domain experts for requirements 
