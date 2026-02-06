# Capstone 1 – Logistics Cost & Delivery Analytics – Dataset Data Dictionary

## shipments_daily.csv (≈ 3,060 rows including duplicates)
- shipment_id (string): Business shipment identifier (duplicates intentionally present)
- warehouse_id (string): Warehouse code (FK -> warehouses.warehouse_id)
- region_id (string): Region code (FK -> regions.region_id) – derived from warehouse for realism
- carrier_id (string, nullable): Carrier code (FK -> carriers.carrier_id). Nulls included intentionally.
- shipment_cost (decimal, nullable): Shipment cost. Nulls + negative/zero + outliers included intentionally.
- delivery_status (string): Delivered / Delayed / Failed
- is_fragile (string): Y/N
- shipment_date (date): Shipment creation date
- delivery_date (date, nullable): Nulls included intentionally (anomalies)
- package_weight_kg (decimal): Package weight
- declared_value_inr (int): Declared value
- payment_type (string): COD / Prepaid / Credit
- priority_level (string): Standard / Express / SameDay
- created_ts (timestamp): Load ordering + dedup “latest wins”

## warehouses.csv (40 rows)
- warehouse_id, warehouse_name, city, state, region_id, capacity_tpd, is_active

## carriers.csv (15 rows)
- carrier_id, carrier_name, mode (Air/Road/Rail/Sea), sla_days (int), is_active

## regions.csv (8 rows)
- region_id, region_name, country

## delivery_events_microbatch.csv (≈ 515 rows including duplicates)
- event_id, shipment_id, event_type, event_ts, location_scan, scan_quality