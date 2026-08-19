# Databricks notebook source
# MAGIC %md
# MAGIC # Quality Check 01: Completeness (NULL Checks)
# MAGIC 
# MAGIC This module implements completeness checks by detecting NULL values in critical fields:
# MAGIC - Customers: email field
# MAGIC - Orders: customer_id and product_id fields
# MAGIC 
# MAGIC Quality flags are added as arrays to track specific issues.

# COMMAND ----------

import dlt
from pyspark.sql.functions import col, when, array, lit, row_number
from pyspark.sql.window import Window

# COMMAND ----------

def add_completeness_flags(df, null_check_columns):
    """
    Add quality flags for NULL value checks.
    
    Args:
        df: Input DataFrame
        null_check_columns: List of column names to check for NULL values
    
    Returns:
        DataFrame with quality_flags array column added
    """
    quality_flag_expr = array()
    
    for col_name in null_check_columns:
        quality_flag_expr = when(
            col(col_name).isNull(),
            array(lit(f"NULL_{col_name}"))
        ).otherwise(array())
    
    return df.withColumn("completeness_flags", quality_flag_expr)