# Logistics Cost & Delivery Analytics Platform  
**Azure Data Engineering Capstone Project**

## Overview
This project demonstrates an **end-to-end Azure Data Engineering solution** built to analyze logistics shipment costs, delivery performance, and carrier SLAs using a **Medallion Architecture (Bronze → Silver → Gold)**.

The solution ingests batch and near-real-time data, applies data quality and cleansing rules, models data into a **BI-optimized star schema**, and exposes insights through **Power BI dashboards**.

The project is designed as a **real-world enterprise scenario**, emphasizing:
- Data quality governance
- Incremental ingestion patterns
- Scalable lakehouse design
- Analytics-ready modeling

---

## Problem Statement
Regional warehouses generate daily shipment extracts. Business leadership requires:
- Shipment cost governance and anomaly detection  
- Delivery performance tracking by region, warehouse, and carrier  
- SLA adherence and fragile shipment monitoring  
- A trusted, reusable semantic model for analytics  

This project builds a platform that converts raw logistics data into **decision-ready insights**.

---

## Architecture & Tech Stack

### Azure Services Used
- **Azure Data Lake Storage Gen2** – Raw and curated data zones  
- **Azure Data Factory (ADF)** – Batch ingestion, orchestration, watermarking  
- **Azure Databricks** – Data cleaning, transformations, Delta Lake, modeling  
- **Power BI** – Semantic model and dashboards  

### Architecture Pattern
- **Medallion Architecture**
  - **Bronze**: Raw CSV data (as-is)
  - **Silver**: Cleaned, deduplicated, DQ-validated Delta tables
  - **Gold**: Star schema optimized for BI consumption

> 📐 **Architecture Diagram**  
> *(Add link below)*  
> `Architecture Diagram:` **[Link Here]**

---

---

## Datasets

| Dataset | Description |
|------|-----------|
| `shipments_daily.csv` | Daily shipment transactions (~3,000 rows) |
| `warehouses.csv` | Warehouse master data |
| `carriers.csv` | Carrier reference data |
| `regions.csv` | Region reference data |
| `delivery_events_microbatch.csv` | Optional near-real-time delivery events |

> 📂 **Main Dataset Location**  
> `Data Files:` **[Link to data folder / ADLS snapshot]**

---

## Data Quality & Cleansing Rules
Key data challenges are intentionally embedded:
- Null or missing shipment cost  
- Duplicate shipment records  
- Carrier reference mismatches  
- Cost outliers (10× normal values)  
- Date anomalies (delivery before shipment, missing delivery dates)  

All rules are applied in the **Silver layer**, with:
- DQ flags in fact data
- Quarantine routing for invalid records
- Daily DQ summary metrics

> 📘 **Data Dictionary & DQ Rules**  
> - Data Dictionary: **[Link Here]**  
> - Data Quality Rules: **[Link Here]**

---

## Data Model (Gold Layer)

### Dimensions
- `DimDate`
- `DimWarehouse`
- `DimRegion`
- `DimCarrier`

### Fact
- `FactShipments`

The model follows **star schema best practices** for Power BI:
- Surrogate keys
- Unknown dimension handling
- Incremental Delta MERGE patterns

> 🧱 **Star Schema Design**  
> `Model Diagram:` **[Link Here]**

---

## Pipelines & Processing

### Ingestion (ADF)
- Parameterized daily ingestion
- Watermark / incremental loading
- File existence and row-count validation
- Pipeline run logging

### Transformation (Databricks)
- Bronze → Silver: Cleaning, typing, deduplication, DQ flags
- Silver → Gold: Dimensional modeling, surrogate keys
- Optional Auto Loader for micro-batch ingestion

> 🔄 **ADF Pipeline Details**  
> `ADF Pipelines:` **[Link Here]**

---

## Analytics & Dashboards

### KPIs Delivered
- Total Shipment Cost (DQ-validated)
- Cost by Region / Warehouse / Carrier
- On-time Delivery %
- SLA Compliance
- Fragile Shipment Performance
- Data Quality Metrics

> 📊 **Power BI Dashboard**  
> `Dashboard Link / Screenshots:` **[Link Here]**

---

## Validation & Reconciliation
- Row count reconciliation across Bronze, Silver, Gold
- DQ rule counts by day and warehouse
- Data freshness checks
- Business KPI validation

> ✅ **Validation Report**  
> `Validation Outputs:` **[Link Here]**

---

## Project Documentation
- 📄 **Project Description (Google Doc):** [Add Link]
- 📘 **Data Dictionary:** [Add Link]
- 📐 **Architecture Diagram:** [Add Link]
- 🔄 **Pipeline Runbook:** [Add Link]
- 📊 **Power BI Report:** [Add Link]

---

## Team & Timeline
- **Duration:** 40 hours (5 days × 8 hours)
- **Team Size:** 5
- **Delivery Model:** Sprint-based execution

---

## Key Takeaways
- Implements industry-standard **Azure Lakehouse architecture**
- Demonstrates strong **data engineering best practices**
- Focuses on **data quality, governance, and BI performance**
- Designed to be **scalable, auditable, and production-ready**

---

## Future Enhancements
- Streaming ingestion via Event Hub
- CI/CD with Azure DevOps
- Automated DQ alerts
- Cost optimization and performance benchmarking

---

