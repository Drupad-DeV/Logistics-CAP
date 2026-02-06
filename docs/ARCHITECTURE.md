# Pipeline Architecture

## Overview

The Logistics Data Engineering Pipeline is designed with a modular architecture that separates concerns and allows for easy extension and maintenance.

## Components

### 1. Data Ingestion (`data_ingestion.py`)

**Purpose**: Load raw CSV data into memory for processing

**Key Features**:
- CSV file loading with pandas
- Support for multiple file loading
- Data information extraction
- Error handling for missing files

### 2. Data Cleaning (`data_cleaning.py`)

**Purpose**: Transform and clean raw data

**Key Features**:
- Duplicate removal
- Missing value handling (drop, fill, interpolate)
- Text standardization
- Data type conversion
- Outlier detection and removal

### 3. Data Validation (`data_validation.py`)

**Purpose**: Validate data quality and schema compliance

**Key Features**:
- Schema validation
- Data type checking
- Quality metrics calculation
- Value range validation

### 4. ETL Pipeline (`etl_pipeline.py`)

**Purpose**: Orchestrate the complete data pipeline

**Key Features**:
- Configuration-driven pipeline
- Step-by-step execution with logging
- Integration of all components
- Summary reporting

## Data Flow

1. **Configuration Loading**: Load pipeline configuration from YAML
2. **Extract Phase**: Read raw CSV from `data/raw/`
3. **Validate Phase (Initial)**: Check schema and calculate quality metrics
4. **Transform Phase**: Clean and transform the data
5. **Validate Phase (Final)**: Re-check data quality
6. **Load Phase**: Save cleaned data to `data/cleaned/`

## Configuration

Pipeline behavior is controlled via `config/pipeline_config.yaml`

## Extension Points

You can extend the pipeline by:
- Adding new cleaning operations to `DataCleaner`
- Adding new validation rules to `DataValidator`
- Modifying the pipeline flow in `ETLPipeline`
