# Capstone 1 – Logistics Cost & Delivery Analytics  
## Updated Dataset Data Dictionary (Post Scale-Up)

---

## Overview

This data dictionary documents the **final dataset state** after scaling the fact table by appending synthetic data while preserving schema, foreign-key integrity, and business realism.

- Architecture: ADLS Gen2 + ADF + Databricks + Power BI  
- Pattern: Medallion (Bronze → Silver → Gold)  
- Modeling Target: Star Schema  
- Validation: Referential integrity enforced using distinct FK domain comparison  

---

## FACT TABLE

### shipments_daily.csv

**Role:** Fact table (shipment transactions)  
**Grain:** 1 row = 1 shipment  
**Source:**  
- Original daily extract (~3,060 rows, including duplicates)  
- Appended synthetic data (incremental, scalable)

**Current Volume:**  
- Original: ~3,060 rows  
- Appended: Configurable (500K / 1M / up to ~2.5M)  
- Total: Original + Appended rows

---

### Fact Columns

| Column Name | Data Type | Nullable | Description |
|------------|----------|----------|------------|
| shipment_id | string | No | Business shipment identifier; duplicates intentionally present |
| warehouse_id | string | No | Warehouse code (FK → warehouses.warehouse_id) |
| region_id | string | No | Region code (FK → regions.region_id) |
| carrier_id | string | Yes | Carrier code (FK → carriers.carrier_id); ~5% NULLs allowed |
| shipment_cost | decimal | Yes | Shipment cost; NULLs, zero/negative, and outliers included |
| delivery_status | string | No | Delivered / In Transit / Delayed |
| is_fragile | string | No | Y / N |
| shipment_date | date | No | Shipment creation date |
| delivery_date | date | Yes | Delivery date; derived from shipment_date + delivery_days |
| package_weight_kg | decimal | No | Package weight in kilograms |
| declared_value_inr | decimal | No | Declared shipment value (INR) |
| payment_type | string | No | Prepaid / COD |
| priority_level | string | No | Low / Medium / High |
| created_ts | timestamp | No | Record creation timestamp (ordering, dedup support) |
| delivery_days | int | No | Delivery duration in days (generated; originally NULL) |

---

## DIMENSION TABLES

### warehouses.csv

**Rows:** 40  
**Role:** Warehouse dimension

| Column |
|-------|
| warehouse_id (PK) |
| warehouse_name |
| city |
| state |
| region_id (FK → regions.region_id) |
| capacity_tpd |
| is_active |

---

### carriers.csv

**Rows:** 15  
**Role:** Carrier / logistics partner dimension

| Column |
|-------|
| carrier_id (PK) |
| carrier_name |
| mode (Air / Road / Rail / Sea) |
| sla_days |
| is_active |

---

### regions.csv

**Rows:** 8  
**Role:** Geographic dimension

| Column |
|-------|
| region_id (PK) |
| region_name |
| country |

---

### delivery_events_microbatch.csv

**Rows:** ~515  
**Role:** Near-real-time delivery events (optional enrichment)

| Column |
|-------|
| event_id |
| shipment_id (FK → shipments_daily.shipment_id) |
| event_type |
| event_ts |
| location_scan |
| scan_quality |

---

## Data Generation & Scale-Up Rules

### Volume Rules
- Fact data scaled by **appending**, not replacing
- Incremental growth supported (ADF-style ingestion)
- Duplicates intentionally retained for dedup testing

---

### Foreign Key Integrity Rules
- No new foreign-key values introduced
- All non-null FKs must exist in dimension tables
- Validation performed using **distinct FK vs dim key anti-joins**

| Fact Column | Dimension |
|------------|-----------|
| warehouse_id | warehouses |
| region_id | regions |
| carrier_id | carriers (NULL allowed) |

---

### shipment_id Rules
- Format preserved (SHPxxxxx)
- Mostly unique
- ~0.5–1% exact duplicates retained

---

### Date & Time Rules

**shipment_date**
- Spread across multiple months
- No future dates

**delivery_days**
- Originally entirely NULL in source data
- Generated randomly (1–7 days)

**delivery_date**
- Derived as shipment_date + delivery_days
- Nullable anomalies allowed

**created_ts**
- Same day or slightly before shipment_date
- Supports incremental processing and dedup logic

---

### shipment_cost Rules
- Majority between INR 50–5,000
- ~3–5% NULL values
- ~1% high outliers
- Small percentage zero/negative values

---

### package_weight_kg Rules
- Typical range: 0.5–50 kg
- Outliers allowed for realism

---

### declared_value_inr Rules
- Range: INR 500–500,000
- Loosely correlated with priority and weight

---

### delivery_status Distribution

| Status | Approximate Percentage |
|------|------------------------|
| Delivered | 85–90% |
| In Transit | 8–12% |
| Delayed | 2–5% |

---

### is_fragile Rules
- Approximately 25% of shipments marked fragile

---

### payment_type Distribution

| Type | Percentage |
|----|------------|
| Prepaid | ~65% |
| COD | ~35% |

---

### priority_level Distribution

| Level | Percentage |
|------|------------|
| Low | ~50% |
| Medium | ~35% |
| High | ~15% |

---

### Intentional Data Skew
- Top 5 warehouses handle ~60% of volume
- 2–3 carriers dominate shipment volume
- Metro regions show higher shipment density

---

## Validation Guarantees

- Referential integrity validated using distinct-domain comparisons
- Schema unchanged from original contract
- Append-safe for ADLS / ADF
- Ready for Silver-layer DQ checks and Gold star-schema modeling

---
