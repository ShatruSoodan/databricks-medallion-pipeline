# Databricks notebook source
# MAGIC %md
# MAGIC # Quality Check 02: Uniqueness (Duplicate Detection)
# MAGIC 
# MAGIC This module implements uniqueness checks by detecting duplicate values in primary key fields:
# MAGIC - Customers: customer_id
# MAGIC - Orders: order_id
# MAGIC 
# MAGIC Uses window functions to count occurrences and flag duplicates.

# COMMAND ----------

import dlt
from pyspark.sql.functions import col, when, array, lit, row_number, count
from pyspark.sql.window import Window

# COMMAND ----------

def add_uniqueness_flags(df, unique_key_column):
    """
    Add quality flags for duplicate key detection.
    
    Args:
        df: Input DataFrame
        unique_key_column: Column name that should be unique
    
    Returns:
        DataFrame with uniqueness_flags array column added
    """
    # Add window to count occurrences of each key
    window_spec = Window.partitionBy(unique_key_column)
    
    df = df.withColumn(
        f"{unique_key_column}_count",
        count(unique_key_column).over(window_spec)
    )
    
    # Flag duplicates
    df = df.withColumn(
        "uniqueness_flags",
        when(
            col(f"{unique_key_column}_count") > 1,
            array(lit(f"DUPLICATE_{unique_key_column}"))
        ).otherwise(array())
    )
    
    return df.drop(f"{unique_key_column}_count")