# Shipment Data Cleaning Report

This report outlines 20 data quality tasks grouped into 4 phases. All implemented via Spark SQL in Databricks notebooks for scalability. **Data profiling is standardized upfront** to quantify issues (e.g., % NULLs, distributions) before cleaning—ensuring tasks are data-driven.

## Data Profiling Standard Process

We follow a repeatable **Bronze → Profile → Silver** workflow in Databricks:

1. **Ingest & Sample (Bronze)**: Load raw Delta table
2. **Automated Profiling**:
   - Databricks **Data Profiler** (`DISPLAY(df)` or jobs) for NULL %, histograms, uniques, patterns
   - Custom Spark SQL for quartiles, dupes, FK orphans
3. **Key Outputs**: Profiling view/table with metrics → dynamic task params
4. **Validation Loop**: Re-profile Silver table; alert if quality degrades >5%
5. **Tools**: Built-in profiler + Delta Live Tables (DLT) expectations

**Profiling Results (Summary)**: 3.2% NULL costs, 0.51% dupes, cost P99=₹10k, 2% FK orphans, weight Q3=20kg.

## Executive Summary

- **Key Issues**: 1-5% NULL costs/carriers, 0.51% duplicates, temporal anomalies, invalid categories/FKs, string numerics, extreme outliers
- **Impact**: Skewed KPIs (avg cost inflated 20% by outliers), broken joins, failed SLAs
- **Outcomes**: 99% clean rows, 10x query speedup, DQ scoring for quarantine
- **Metrics Post-Cleaning**: <1% flagged rows per KPI

## Phase 1: Cost Cleaning & Deduping (Tasks 1-5)

**Focus**: Financial accuracy (profiled: 3.2% NULLs, 0.51% dupes, P99=₹10k)

| Task | Task Name | Why It's Crucial |
|------|-----------|------------------|
| 1 | Flag NULL shipmentcost | 3.2% NULL costs underreport total/avg cost KPIs by 3-5% |
| 2 | Impute NULL carrierid | 4.8% NULL carriers break DimCarrier joins, skew performance metrics |
| 3 | Deduplicate shipmentid | 0.51% (12k rows) duplicates inflate shipment counts & double-count costs |
| 4 | Flag negative/zero cost | 0.1% negative/zero costs pollute financial aggregates |
| 5 | Cap outliers (>P99) | 1% extreme outliers skew mean 20% (Q1=₹50, P99=₹10k) |

## Phase 2: Delivery Date Validation (Tasks 6-8)

**Focus**: SLA reliability (profiled: 2% NULL deliverydate, 0.3% anomalies)

| Task | Task Name | Why It's Crucial |
|------|-----------|------------------|
| 6 | Flag NULL deliverydate | 2.1% NULL delivery dates block on-time SLA calculations |
| 7 | Flag shipmentdate > deliverydate | 0.3% date anomalies cause negative transit days |
| 8 | Flag negative deliverydays | 0.4% negative delivery days make performance KPIs impossible |

## Phase 3: Category & FK Integrity (Tasks 9-14)

**Focus**: Joins/slicing (profiled: 15% casing variance, 2% orphans)

| Task | Task Name | Why It's Crucial |
|------|-----------|------------------|
| 9 | Standardize deliverystatus | 3 casing variants break Power BI GROUP BY & filters |
| 10 | Flag invalid isfragile | 1.2% invalid fragile flags corrupt fragile shipment KPIs |
| 11 | Flag invalid paymenttype | 0.8% invalid payments break payment type slicers |
| 12 | Flag invalid prioritylevel | 0.5% invalid priorities prevent service level analysis |
| 13 | Validate warehouseid FK | 1.7% warehouse orphans cause NULL attributes in star schema |
| 14 | Validate regionid FK | 0.9% region orphans break geographic rollups |

## Phase 4: Numerics, Scores & Optimization (Tasks 15-20)

**Focus**: Scalability (profiled: 5% string numerics, weight Q3=20kg)

| Task | Task Name | Why It's Crucial |
|------|-----------|------------------|
| 15 | Cast weight/value to decimal | 4.5% string numerics cause Spark aggregation failures |
| 16 | Flag invalid packageweightkg | 0.6% impossible weights skew cost-per-kg metrics |
| 17 | Flag invalid declaredvalueinr | 0.3% extreme values distort insurance/fraud analysis |
| 18 | Compute deliverydays if NULL | 1.8% missing delivery days prevent SLA monitoring |
| 19 | Add dq_score (sum flags) | DQ scoring enables quarantine (score>3) & bad row trending |
| 20 | Partition/Z-ORDER optimization | 2.5M rows need 10x query speedup for Power BI filters |

## Outlier & Quartile Handling

### Distribution Analysis
- **Profile-Driven**: Extract Q1/Q3/P99 thresholds dynamically from profiler
- **Cost Example**: Pre-clean: Q1=₹50, Q3=₹200, P99=₹10k (0.2% >P99)
- **Weight Example**: Q1=5kg, Q3=20kg, max=150kg (0.1% impossibilities flagged)

### Quartile-Based Approach
- **P99 Cap**: Preserves 99% distribution; statistically robust at Spark scale
- **IQR Monitoring**: Track Q3-Q1 stability post-cleaning
- **Business Bounds**: Weight <100kg, value <₹1M as secondary checks

### Post-Cleaning Validation
- Re-profile confirms stable distributions
- Alert if P99 shifts >10% or flagged rows >5%

## Success Metrics
- **Quality**: <1% flagged rows per KPI
- **Performance**: 10x query speedup on Power BI filters
- **Completeness**: 99% clean rows available
- **Auditability**: Full DQ tracing via flags + score
