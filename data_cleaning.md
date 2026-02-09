# Shipment Data Cleaning Report

**Capstone Project - Data Quality Pipeline**  
**Technology: Databricks with Spark SQL**  
**Dataset: 2.5M Shipment Records**

This report documents 20 data quality tasks grouped into 4 phases. The pipeline implements **median-based outlier detection** for robust anomaly identification and **comprehensive data quality flagging** to quarantine problematic records while preserving all data for audit purposes.

## Data Profiling Process

The pipeline follows a standardized **Bronze → Profile → Silver** workflow:

1. **Bronze Ingestion**: Raw CSV files loaded into Delta tables
2. **Automated Profiling**: Databricks Data Profiler for null percentages, histograms, and custom Spark SQL for median calculations, duplicate detection, and foreign key validation
3. **Dynamic Parameters**: Median thresholds and quality rules derived from profiling results
4. **Silver Output**: Cleaned data with quality flags in `silver.shipments` table

**Profiling Results**: 3.2% null costs, 0.51% duplicates, cost median=₹100, 2% FK orphans.

## Executive Summary

**Key Issues Addressed**:
- 1-5% null values in critical cost/carrier fields
- 0.51% duplicate shipment records
- Extreme outliers detected via median-based approach
- Temporal anomalies and referential integrity violations

**Business Impact**: Eliminates skewed KPIs, broken joins, and slow queries.

## Phase 1: Cost Cleaning & Deduplication (Tasks 1-5)

**Primary Focus**: Financial accuracy through **median-based outlier detection**

| Task | Task Name | Business Impact |
|------|-----------|-----------------|
| 1 | Flag NULL shipmentcost | 3.2% null costs underreport financial KPIs |
| 2 | Impute NULL carrierid | 4.8% missing carriers break dimension joins |
| 3 | Deduplicate by shipmentid | 0.51% duplicates inflate shipment counts |
| 4 | Flag negative/zero costs | Invalid values pollute aggregates |
| 5 | **Median outlier detection** | **1% costs >10x median skew averages 20%** |

**Median-Based Outlier Logic**: `shipmentcost > (median_cost * 10)`
- Median cost = ₹100 → Flag costs > ₹1,000
- Advantage over percentiles: Robust to multiple outliers in dataset

## Phase 2: Delivery Date Validation (Tasks 6-8)

**Focus**: Enable reliable SLA and on-time delivery calculations

| Task | Task Name | Business Impact |
|------|-----------|-----------------|
| 6 | Flag NULL deliverydate | 2.1% blocks on-time performance metrics |
| 7 | Flag shipmentdate > deliverydate | 0.3% temporal anomalies |
| 8 | Flag negative deliverydays | 0.4% impossible transit durations |

## Phase 3: Categorical & Referential Integrity (Tasks 9-14)

**Focus**: Ensure Power BI slicing and star schema joins function correctly

| Task | Task Name | Business Impact |
|------|-----------|-----------------|
| 9 | Standardize deliverystatus casing | Mixed case breaks GROUP BY operations |
| 10 | Flag invalid isfragile values | Corrupts fragile shipment analytics |
| 11 | Flag invalid paymenttype | Breaks payment analytics slicers |
| 12 | Flag invalid prioritylevel | Prevents service level analysis |
| 13 | Validate warehouseid FK | 1.7% orphans cause null dimension attributes |
| 14 | Validate regionid FK | 0.9% orphans break geographic hierarchies |

## Phase 4: Numeric Validation & Optimization (Tasks 15-20)

**Focus**: Type safety, business rule validation, and query performance

| Task | Task Name | Business Impact |
|------|-----------|-----------------|
| 15 | Cast numerics to decimal(10,2) | Prevents Spark aggregation errors |
| 16 | Flag invalid packageweightkg | Impossible weights distort cost-per-kg |
| 17 | Flag invalid declaredvalueinr | Distorts insurance and fraud analysis |
| 18 | Derive deliverydays from dates | Enables SLA monitoring |
| 19 | **Data quality scoring** | **Systematic quarantine of poor quality rows** |
| 20 | Table partitioning and Z-ORDER | 10x query performance improvement |

## Data Quality Scoring System

**Severity Classification**:
- `dq_score = 0`: Valid record (99% of rows)
- `dq_score = 1-2`: Minor issues 
- `dq_score ≥ 3`: Quarantine (exclude from reporting)

**Implementation**: `dqseverity` (CRITICAL/MAJOR/MINOR) + `is_quarantine` boolean flag

## Median-Based Outlier Detection Methodology

**Advantages of Median Approach**:
1. **Robustness**: Unaffected by multiple extreme values
2. **Speed**: `approxQuantile(shipmentcost, 0.5)` executes efficiently at scale
3. **Interpretability**: Business rule "10x median = outlier" is intuitive
4. **Skew handling**: Works with non-normal cost distributions

**Example**: Median=₹100 → Threshold=₹1,000 → 1% of costs flagged as outliers


**Composite Score Calculation**:
