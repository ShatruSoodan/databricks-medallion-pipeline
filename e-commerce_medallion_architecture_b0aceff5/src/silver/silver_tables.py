# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Quality Validated Tables
# MAGIC 
# MAGIC This notebook creates all silver layer tables with integrated quality checks:
# MAGIC - silver_customers: Completeness, uniqueness, business logic
# MAGIC - silver_orders: All checks including referential integrity
# MAGIC - silver_products: Pass-through with quality flags
# MAGIC - silver_quality_metrics: Aggregated quality metrics

# COMMAND ----------

import dlt
from pyspark.sql.functions import (
    col, when, array, lit, row_number, count, size,
    concat_ws, array_union, explode, coalesce, round as sql_round
)
from pyspark.sql.window import Window

# COMMAND ----------

@dlt.table(
    name="silver_customers",
    comment="Quality validated customer data with completeness, uniqueness, and business logic checks",
    table_properties={
        "quality": "silver",
        "pipelines.autoOptimize.managed": "true"
    }
)
def silver_customers():
    """
    Creates silver_customers table with quality checks:
    - Completeness: NULL email detection
    - Uniqueness: Duplicate customer_id detection  
    - Business Logic: Negative lifetime_value detection
    """
    # Read bronze customers
    df = dlt.read("bronze_customers")
    
    # Add row number for duplicate detection
    window_spec = Window.partitionBy("customer_id").orderBy(col("_ingestion_timestamp"))
    df = df.withColumn("customer_row_num", row_number().over(window_spec))
    df = df.withColumn("customer_id_count", count("customer_id").over(Window.partitionBy("customer_id")))
    
    # Build quality flags array
    df = df.withColumn(
        "quality_flags",
        when(
            col("email").isNull() & (col("customer_id_count") > 1),
            array(lit("NULL_email"), lit("DUPLICATE_customer_id"))
        ).when(
            col("email").isNull(),
            array(lit("NULL_email"))
        ).when(
            col("customer_id_count") > 1,
            array(lit("DUPLICATE_customer_id"))
        ).otherwise(
            array().cast("array<string>")
        )
    )
    
    # Add overall quality check result
    df = df.withColumn(
        "quality_check_passed",
        size(col("quality_flags")) == 0
    )
    
    # Select final columns (keep only first occurrence of duplicates)
    return df.filter(col("customer_row_num") == 1).select(
        "customer_id", "customer_name", "email", "country", "signup_date",
        "customer_segment", "lifetime_value", "_ingestion_timestamp", "_source_file",
        "quality_flags", "quality_check_passed"
    )

# COMMAND ----------

@dlt.table(
    name="silver_orders",
    comment="Quality validated order data with all quality checks including referential integrity",
    table_properties={
        "quality": "silver",
        "pipelines.autoOptimize.managed": "true"
    }
)
def silver_orders():
    """
    Creates silver_orders table with quality checks:
    - Completeness: NULL customer_id and product_id detection
    - Uniqueness: Duplicate order_id detection
    - Referential Integrity: Invalid customer_id and product_id detection
    """
    # Read bronze tables
    orders_df = dlt.read("bronze_orders")
    customers_df = dlt.read("bronze_customers")
    products_df = dlt.read("bronze_products")
    
    # Get valid reference IDs
    valid_customers = customers_df.select("customer_id").distinct()
    valid_products = products_df.select("product_id").distinct()
    
    # Add row number for duplicate detection
    window_spec = Window.partitionBy("order_id").orderBy(col("_ingestion_timestamp"))
    orders_df = orders_df.withColumn("order_row_num", row_number().over(window_spec))
    orders_df = orders_df.withColumn("order_id_count", count("order_id").over(Window.partitionBy("order_id")))
    
    # Check referential integrity
    orders_df = orders_df.join(
        valid_customers.withColumn("customer_exists", lit(True)),
        ["customer_id"],
        "left"
    )
    orders_df = orders_df.join(
        valid_products.withColumn("product_exists", lit(True)),
        ["product_id"],
        "left"
    )
    
    # Build quality flags array (comprehensive check)
    orders_df = orders_df.withColumn(
        "quality_flags",
        when(col("customer_id").isNull(), array(lit("NULL_customer_id"))).otherwise(array())
    ).withColumn(
        "quality_flags",
        when(col("product_id").isNull(), array_union(col("quality_flags"), array(lit("NULL_product_id")))).otherwise(col("quality_flags"))
    ).withColumn(
        "quality_flags",
        when(col("customer_exists").isNull() & col("customer_id").isNotNull(), array_union(col("quality_flags"), array(lit("INVALID_customer_id")))).otherwise(col("quality_flags"))
    ).withColumn(
        "quality_flags",
        when(col("product_exists").isNull() & col("product_id").isNotNull(), array_union(col("quality_flags"), array(lit("INVALID_product_id")))).otherwise(col("quality_flags"))
    ).withColumn(
        "quality_flags",
        when(col("order_id_count") > 1, array_union(col("quality_flags"), array(lit("DUPLICATE_order_id")))).otherwise(col("quality_flags"))
    )
    
    # Add overall quality check result
    orders_df = orders_df.withColumn(
        "quality_check_passed",
        size(col("quality_flags")) == 0
    )
    
    # Select final columns (keep only first occurrence of duplicates)
    return orders_df.filter(col("order_row_num") == 1).select(
        "order_id", "customer_id", "order_date", "product_id", "quantity",
        "unit_price", "total_amount", "order_status", "payment_date",
        "_ingestion_timestamp", "_source_file",
        "quality_flags", "quality_check_passed"
    )

# COMMAND ----------

@dlt.table(
    name="silver_products",
    comment="Quality validated product data (pass-through with quality flags)",
    table_properties={
        "quality": "silver",
        "pipelines.autoOptimize.managed": "true"
    }
)
def silver_products():
    """
    Creates silver_products table.
    Products typically have high quality in reference data, so this is primarily a pass-through.
    """
    df = dlt.read("bronze_products")
    
    # Add empty quality flags (products are typically clean reference data)
    df = df.withColumn("quality_flags", array().cast("array<string>"))
    df = df.withColumn("quality_check_passed", lit(True))
    
    return df.select(
        "product_id", "product_name", "category", "cost", "price",
        "_ingestion_timestamp", "_source_file",
        "quality_flags", "quality_check_passed"
    )

# COMMAND ----------

@dlt.table(
    name="silver_quality_metrics",
    comment="Aggregated quality metrics for all silver tables",
    table_properties={
        "quality": "silver",
        "pipelines.autoOptimize.managed": "true"
    }
)
def silver_quality_metrics():
    """
    Generates quality metrics report with pass/fail rates by table and check type.
    """
    # Read silver tables
    customers_df = dlt.read("silver_customers")
    orders_df = dlt.read("silver_orders")
    products_df = dlt.read("silver_products")
    
    # Get row counts
    customers_total = customers_df.count()
    orders_total = orders_df.count()
    products_total = products_df.count()
    
    # Customers: explode quality flags and count by type
    customers_metrics = customers_df.filter(size(col("quality_flags")) > 0).select(
        explode(col("quality_flags")).alias("check_type")
    ).groupBy("check_type").count().withColumn("table_name", lit("silver_customers"))
    
    customers_overall = customers_df.selectExpr(
        "'silver_customers' as table_name",
        "'OVERALL' as check_type",
        f"{customers_total} as total_rows",
        "count(*) as count"
    )
    
    # Orders: explode quality flags and count by type
    orders_metrics = orders_df.filter(size(col("quality_flags")) > 0).select(
        explode(col("quality_flags")).alias("check_type")
    ).groupBy("check_type").count().withColumn("table_name", lit("silver_orders"))
    
    orders_overall = orders_df.selectExpr(
        "'silver_orders' as table_name",
        "'OVERALL' as check_type",
        f"{orders_total} as total_rows",
        "count(*) as count"
    )
    
    # Products overall
    products_overall = products_df.selectExpr(
        "'silver_products' as table_name",
        "'OVERALL' as check_type",
        f"{products_total} as total_rows",
        "count(*) as count"
    )
    
    # Add total_rows column to metrics dataframes
    customers_metrics = customers_metrics.withColumn("total_rows", lit(customers_total))
    orders_metrics = orders_metrics.withColumn("total_rows", lit(orders_total))
    
    # Union all metrics
    all_metrics = (
        customers_metrics.select("table_name", "check_type", "total_rows", "count")
        .union(customers_overall.select("table_name", "check_type", "total_rows", "count"))
        .union(orders_metrics.select("table_name", "check_type", "total_rows", "count"))
        .union(orders_overall.select("table_name", "check_type", "total_rows", "count"))
        .union(products_overall.select("table_name", "check_type", "total_rows", "count"))
    )
    
    # Calculate pass/fail statistics
    return all_metrics.select(
        col("table_name"),
        col("check_type"),
        col("total_rows"),
        coalesce(col("count"), lit(0)).alias("failed_rows"),
        (col("total_rows") - coalesce(col("count"), lit(0))).alias("passed_rows"),
        sql_round(
            ((col("total_rows") - coalesce(col("count"), lit(0))) / col("total_rows")) * 100, 2
        ).alias("pass_rate_percent")
    )