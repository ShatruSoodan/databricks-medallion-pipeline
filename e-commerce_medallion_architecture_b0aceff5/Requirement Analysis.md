# Requirement Analysis

## Problem Statement
An e-commerce company ingests daily sales data from multiple sources (customer database, order system, product catalog) into Databricks. They need to:
Bronze Layer: Ingest raw CSV files from S3/DBFS
Silver Layer: Apply data quality checks, clean and validate data
Gold Layer: Create business-ready aggregations for analytics
Dashboard: BI dashboards for business stakeholders

## Functional Requirements
✅ A working end-to-end pipeline (Bronze → Silver → Gold → Dashboard)
✅ Sample data generator with realistic quality issues
✅ All four quality checks implemented and working
✅ All three Gold layer aggregations
✅ Dashboard with 3+ SQL queries and visualizations
✅ Database schema/setup script and seed data
✅ README with working setup instructions
✅ Basic test suite (data quality tests, pipeline integration tests)
✅ Full prompt history with all AI interactions documented
✅ Requirement analysis, design notes, test strategy
✅ Debugging notes and code review notes

## Assumptions
- All Functional Requirements should be done by AI Agent only

## Clarifications Needed
Part B: Medallion Architecture Data Pipeline Project — Details
Objective
Demonstrate practical AI-assisted delivery through a realistic Medallion Architecture data engineering assignment. 
Business Context
Problem Statement:
An e-commerce company ingests daily sales data from multiple sources (customer database, order system, product catalog) into Databricks. They need to:
Bronze Layer: Ingest raw CSV files from S3/DBFS
Silver Layer: Apply data quality checks, clean and validate data
Gold Layer: Create business-ready aggregations for analytics
Dashboard: BI dashboards for business stakeholders
Common Technical Requirements
Whichever option you choose, every submission must include:
✅ Sample data generator script (creates realistic CSV files with intentional quality issues)
✅ Bronze layer ingestion code (Python/PySpark)
✅ Silver layer validation code (all 4 quality checks working)
✅ Gold layer aggregation code (all 4 aggregations)
✅ Dashboard queries (3+ SQL queries for visualizations)
✅ Database schema or setup script
✅ Seed/sample data (customers, orders, products CSVs)
✅ Input validation and error handling
✅ Data quality reporting
✅ At least one meaningful test tier (data quality tests, pipeline tests)
✅ README setup instructions
✅ Full prompt history (CRITICAL)
✅ All planning, design, testing, debugging, and reflection artifacts in the repository
The full set of lifecycle artifacts is required regardless of stretch tier. Only the application scope is small — the artifacts are the point.
Data Schema & Technical Setup
Source Files (S3/DBFS CSVs)
Table 1: customers.csv
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
Core Logic for Bronze to Gold layer
Five main components:
1. Sample Data Generation
Use Cursor to help design a Python/PySpark script
Generate all three CSVs with realistic data
Intentionally introduce the quality issues listed above
Document how data was generated and why quality issues exist
2. Bronze Layer — Ingestion
Read CSVs from S3/DBFS into Databricks
Create Bronze tables (raw, unchanged data)
Handle schema inference and data types
Log ingestion metadata (row counts, timestamp)
No transformations or cleaning — just raw ingest
3. Silver Layer — Data Quality & Validation
Implement below quality checks:
Completeness: No NULLs in critical fields (email, customer_id, product_id)
Uniqueness: No duplicate rows (order_id, customer_id)
Referential Integrity: Foreign keys exist (every customer_id, every product_id)
Flag bad rows (don't delete — add quality_check_result column)
Generate quality metrics report (% passed each check)
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
5. BI Dashboard
Create Databricks SQL Dashboard with 3+ tiles
Visualizations: Top 10 products by revenue (bar), Customer revenue distribution (histogram), Customer segmentation (pie)
Write queries, configure visualizations, add filters
Core Acceptance Criteria:
[ ] Sample data generated (3 CSVs with intentional issues)
[ ] Bronze layer ingests all three sources successfully
[ ] Silver layer implements all four quality checks
[ ] Quality report shows % passed for each check
[ ] Gold layer produces all three aggregation tables
[ ] Aggregation calculations are correct (sum, count, avg, etc.)
[ ] Dashboard displays all 3+ visualizations
[ ] All code is readable, commented, documented
[ ] README setup instructions work end-to-end
[ ] Data quality tests pass (verify checks catch intentional issues)

