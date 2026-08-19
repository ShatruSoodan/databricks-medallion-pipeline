# Databricks notebook source
# MAGIC %md
# MAGIC # Quality Check 05: Business Logic Validation
# MAGIC 
# MAGIC This module implements business logic validation checks:
# MAGIC - Order total_amount = unit_price * quantity
# MAGIC - Payment_date >= order_date (if not null)
# MAGIC - Lifetime_value >= 0
# MAGIC - Quantity > 0
# MAGIC 
# MAGIC These are domain-specific rules that ensure data makes business sense.

# COMMAND ----------

import dlt
from pyspark.sql.functions import col, when, array, lit, abs

# COMMAND ----------

def add_business_logic_flags(df, entity_type):
    """
    Add quality flags for business logic violations.
    
    Args:
        df: Input DataFrame
        entity_type: 'orders' or 'customers' to determine which rules to apply
    
    Returns:
        DataFrame with business_logic_flags array column added
    """
    if entity_type == 'orders':
        # Check calculation: total_amount should equal unit_price * quantity
        # Allow small floating point variance (< 0.01)
        df = df.withColumn(
            "calculation_error",
            abs(col("total_amount") - (col("unit_price") * col("quantity"))) > 0.01
        )
        
        # Check quantity > 0
        df = df.withColumn(
            "invalid_quantity",
            col("quantity") <= 0
        )
        
        # Check payment_date >= order_date (if payment_date is not null)
        df = df.withColumn(
            "invalid_payment_date",
            col("payment_date").isNotNull() & (col("payment_date") < col("order_date"))
        )
        
        # Build flags array
        df = df.withColumn(
            "business_logic_flags",
            when(
                col("calculation_error") | col("invalid_quantity") | col("invalid_payment_date"),
                array()
            ).otherwise(array())
        )
        
        df = df.drop("calculation_error", "invalid_quantity", "invalid_payment_date")
        
    elif entity_type == 'customers':
        # Check lifetime_value >= 0
        df = df.withColumn(
            "business_logic_flags",
            when(
                col("lifetime_value") < 0,
                array(lit("NEGATIVE_lifetime_value"))
            ).otherwise(array())
        )
    
    else:
        # Default: no business logic checks
        df = df.withColumn("business_logic_flags", array())
    
    return df