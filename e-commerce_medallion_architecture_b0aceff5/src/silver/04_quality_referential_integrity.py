# Databricks notebook source
# MAGIC %md
# MAGIC # Quality Check 04: Referential Integrity
# MAGIC 
# MAGIC This module implements referential integrity checks to ensure foreign keys are valid:
# MAGIC - Orders.customer_id must exist in Customers.customer_id
# MAGIC - Orders.product_id must exist in Products.product_id
# MAGIC 
# MAGIC Uses left anti joins to identify orphaned records.

# COMMAND ----------

import dlt
from pyspark.sql.functions import col, when, array, lit

# COMMAND ----------

def add_referential_integrity_flags(orders_df, customers_df, products_df):
    """
    Add quality flags for referential integrity violations.
    
    Args:
        orders_df: Orders DataFrame
        customers_df: Customers DataFrame  
        products_df: Products DataFrame
    
    Returns:
        Orders DataFrame with referential_integrity_flags array column added
    """
    # Check customer_id exists
    valid_customer_ids = customers_df.select("customer_id").distinct()
    orders_df = orders_df.withColumn(
        "valid_customer_id",
        col("customer_id").isin(
            [row.customer_id for row in valid_customer_ids.collect()]
        )
    )
    
    # Check product_id exists
    valid_product_ids = products_df.select("product_id").distinct()
    orders_df = orders_df.withColumn(
        "valid_product_id",
        col("product_id").isin(
            [row.product_id for row in valid_product_ids.collect()]
        )
    )
    
    # Build flags array
    orders_df = orders_df.withColumn(
        "referential_integrity_flags",
        when(
            ~col("valid_customer_id") & ~col("valid_product_id"),
            array(lit("INVALID_customer_id"), lit("INVALID_product_id"))
        ).when(
            ~col("valid_customer_id"),
            array(lit("INVALID_customer_id"))
        ).when(
            ~col("valid_product_id"),
            array(lit("INVALID_product_id"))
        ).otherwise(array())
    )
    
    return orders_df.drop("valid_customer_id", "valid_product_id")