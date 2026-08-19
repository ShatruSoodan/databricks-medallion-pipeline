## Architecture Overview
- Bronze → Silver → Gold → Dashboard
## Data Model & Schema
- Table 1: customers.csv
customer_id (INT, Primary Key)
customer_name (STRING)
email (STRING)
country (STRING)
signup_date (DATE)
customer_segment (STRING: Premium/Standard/Basic)
lifetime_value (DECIMAL)
Sample rows: 10,000 customers | File size: ~500 KB
Table 2: orders.csv
order_id (INT, Primary Key)
customer_id (INT, Foreign Key → customers)
order_date (DATE)
product_id (INT, Foreign Key → products)
quantity (INT)
unit_price (DECIMAL)
total_amount (DECIMAL)
order_status (STRING: Pending/Completed/Cancelled)
payment_date (DATE, nullable)
Sample rows: 100,000 orders | File size: ~2-3 MB
Table 3: products.csv
product_id (INT, Primary Key)
product_name (STRING)
category (STRING)
price (DECIMAL)
cost (DECIMAL)
stock_quantity (INT)
reorder_level (INT)
Sample rows: 500 products | File size: ~50 KB
Data Quality Issues (Intentional)
Your sample data should include realistic quality issues for the Silver layer to catch:
customers.csv:
50 rows with NULL email (completeness)
10 rows with duplicate customer_id (uniqueness)
orders.csv:
100 rows with NULL customer_id (completeness)
200 rows with NULL product_id (completeness)
50 rows with customer_id not in customers table (referential integrity)
30 rows with product_id not in products table (referential integrity)
20 duplicate order_id rows (uniqueness)
Total issues: ~700 problematic rows out of ~100,000 (0.7% — realistic data quality)

## Bronze Layer Design
2.Bronze Layer — Ingestion
Read CSVs from S3/DBFS into Databricks
Create Bronze tables (raw, unchanged data)
Handle schema inference and data types
Log ingestion metadata (row counts, timestamp)
No transformations or cleaning — just raw ingest

## Silver Layer Design
3. Silver Layer — Data Quality & Validation
Implement below quality checks:
Completeness: No NULLs in critical fields (email, customer_id, product_id)
Uniqueness: No duplicate rows (order_id, customer_id)
Referential Integrity: Foreign keys exist (every customer_id, every product_id)
Flag bad rows (don't delete — add quality_check_result column)
Generate quality metrics report (% passed each check)

## Gold Layer Design
4. Gold Layer — Aggregations & Analytics
Build three aggregation tables:
A) Sales by Product:
product_id, product_name, category
total_orders, total_revenue, avg_order_value
B) Revenue by Customer:
customer_id, customer_name, customer_segment
total_orders, total_revenue, avg_order_value, lifetime_value_actual
C) Customer Segmentation:
segment_type (High-Value/Repeat/One-Time/Inactive)
customer_count, avg_revenue, total_revenue

## Data Quality Validation Strategy
- As per requiremnt share it with Genie code.
## Debugging Approach
- Share your pipeline path and ask Genie to run and resolve issue.