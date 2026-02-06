# Capstone 1 – Logistics Cost & Delivery Analytics Dataset
## Data Dictionary (Updated Post Scale-Up)

---

## Overview

This document describes the final dataset state after scaling up the original sample by appending synthetic data while maintaining complete schema compatibility, foreign-key integrity, and business realism. 

The dataset follows enterprise patterns:
- **Architecture**: ADLS Gen2 + ADF + Databricks + Power BI
- **Architecture Pattern**: Medallion (Bronze → Silver → Gold) 
- **Modeling Target**: Star Schema
- **Data Quality Validation**: Referential integrity via distinct FK domain comparison

---

## FACT TABLE

### shipments_daily.csv

**Business Role**: Fact table containing shipment transactions  
**Grain**: 1 row = 1 shipment record  
**Data Sources**: 
- Original daily extract (3,060 rows including intentional duplicates)
- Appended synthetic data (configurable scale: 500K / 1M / 2.5M rows)

**Current Volume**: Original rows + appended synthetic rows

### Fact Table Columns

| Column Name | Data Type | Nullable | Description |
|-------------|-----------|----------|-------------|
| `shipment_id` | string | No | Business shipment identifier. Duplicates intentionally present for deduplication testing. |
| `warehouse_id` | string | No | Warehouse code. Foreign key references `warehouses.warehouse_id`. |
| `region_id` | string | No | Region code. Foreign key references `regions.region_id`. Derived from warehouse location. |
| `carrier_id` | string | Yes | Carrier code. Foreign key references `carriers.carrier_id`. Approximately 5% records contain NULL values. |
| `shipment_cost` | decimal | Yes | Shipment cost in INR. Contains NULL values, zero values, negative outliers, and extreme high values for data quality testing. |
| `delivery_status` | string | No | Final delivery status. Values: Delivered / In Transit / Delayed. |
| `is_fragile` | string | No | Fragile flag. Values: Y / N. |
| `shipment_date` | date | No | Date when shipment record was created in the system. |
| `delivery_date` | date | Yes | Actual delivery date. Derived as `shipment_date + delivery_days`. NULL values present in source data. |
| `package_weight_kg` | decimal | No | Package weight measured in kilograms. |
| `declared_value_inr` | decimal | No | Declared shipment value in Indian Rupees. |
| `payment_type` | string | No | Payment collection method. Values: Prepaid / COD. |
| `priority_level` | string | No | Service priority level. Values: Low / Medium / High. |
| `created_ts` | timestamp | No | Record creation timestamp. Used for incremental processing and deduplication (latest record wins). |
| `delivery_days` | int | No | Calculated delivery duration in days. Generated from originally NULL values in source data. |

---

## DIMENSION TABLES

### warehouses.csv

**Row Count**: 40 rows  
**Business Role**: Warehouse dimension (master data)

**Columns**:
- `warehouse_id` (Primary Key)
- `warehouse_name`
- `city`
- `state`
- `region_id` (Foreign Key → `regions.region_id`)
- `capacity_tpd` (Tons Per Day capacity)
- `is_active` (Y/N status flag)

### carriers.csv

**Row Count**: 15 rows  
**Business Role**: Carrier and logistics partner dimension

**Columns**:
- `carrier_id` (Primary Key)
- `carrier_name`
- `mode` (Transport mode: Air / Road / Rail / Sea)
- `sla_days` (Service Level Agreement days)
- `is_active` (Y/N status flag)

### regions.csv

**Row Count**: 8 rows  
**Business Role**: Geographic region dimension

**Columns**:
- `region_id` (Primary Key)
- `region_name`
- `country`

### delivery_events_microbatch.csv

**Row Count**: 515 rows  
**Business Role**: Near-real-time delivery tracking events (streaming microbatch format)

**Columns**:
- `event_id` (Unique event identifier)
- `shipment_id` (Foreign Key → `shipments_daily.shipment_id`)
- `event_type` (Packed / Dispatched / InTransit / Delivered / etc.)
- `event_ts` (Event timestamp)
- `location_scan` (Scan location)
- `scan_quality` (Good / Poor / Unreadable)

---

## Data Generation & Scale-Up Rules

### Volume Scaling Rules
- Fact table scaled using **append-only** pattern (original data preserved)
- Supports incremental ingestion patterns (ADF-style)
- Intentional duplicates retained for deduplication logic testing

### Foreign Key Integrity Rules
- No new foreign-key values introduced beyond existing dimension domains
- All non-NULL foreign keys guaranteed to exist in target dimension tables
- Validation method: DISTINCT FK values vs dimension key anti-join

**Foreign Key Mapping**:
| Fact Column | Dimension Table |
|-------------|----------------|
| `warehouse_id` | `warehouses` |
| `region_id` | `regions` |
| `carrier_id` | `carriers` (NULL values permitted) |

### shipment_id Generation Rules
- Original format preserved: `SHPxxxxx`
- Primarily unique identifiers
- 0.5–1% exact duplicates intentionally retained

### Date & Time Generation Rules

**shipment_date**:
- Distributed across multiple months
- No future dates relative to load date

**delivery_days**:
- Originally entirely NULL in source extract
- Generated using random distribution (1–7 days typical)

**delivery_date**:
- Calculated as `shipment_date + delivery_days`
- NULL anomalies preserved from source

**created_ts**:
- Typically same day or slightly before `shipment_date`
- Supports incremental processing and deduplication logic

### shipment_cost Generation Rules
- Primary range: INR 50–5,000
- 3–5% records contain NULL values
- 1% records contain high outlier values
- Small percentage contain zero or negative values

### package_weight_kg Generation Rules
- Typical business range: 0.5–50 kg
- Outlier values permitted for realism

### declared_value_inr Generation Rules
- Typical range: INR 500–500,000
- Loose business correlation with priority level and package weight

### delivery_status Distribution
| Status | Approximate Percentage |
|--------|------------------------|
| Delivered | 85–90% |
| In Transit | 8–12% |
| Delayed | 2–5% |

### is_fragile Distribution
- Approximately 25% of shipments marked as fragile (Y)

### payment_type Distribution
| Payment Type | Percentage |
|--------------|------------|
| Prepaid | 65% |
| COD | 35% |

### priority_level Distribution
| Priority Level | Percentage |
|----------------|------------|
| Low | 50% |
| Medium | 35% |
| High | 15% |

### Intentional Data Distribution Skew
- Top 5 warehouses handle 60% of total shipment volume
- 2–3 carriers dominate total shipment volume
- Metropolitan regions exhibit higher shipment density

---

## Data Validation Guarantees

- **Schema Compatibility**: Identical to original sample contract
- **Referential Integrity**: Validated using distinct-domain comparisons
- **Append Safety**: Compatible with ADLS Gen2 and ADF incremental patterns
- **Data Quality Ready**: Suitable for Silver-layer DQ validation and Gold-layer star schema modeling

---

**Dataset ready for production pipeline processing and analytics development.**
