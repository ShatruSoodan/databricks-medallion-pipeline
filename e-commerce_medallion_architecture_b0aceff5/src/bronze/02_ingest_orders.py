# Databricks notebook source
import dlt
from pyspark.sql.functions import current_timestamp, lit

@dlt.table(
    name="bronze_orders",
    comment="Raw order data ingested from CSV with audit columns",
    table_properties={
        "quality": "bronze",
        "pipelines.autoOptimize.managed": "true"
    }
)
def bronze_orders():
    """
    Ingest raw order data from CSV files in Unity Catalog volume.
    Adds audit columns: _ingestion_timestamp and _source_file.
    """
    return (
        spark.read
        .format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load("/Volumes/workspace/dev/medallion_data/orders.csv")
        .withColumn("_ingestion_timestamp", current_timestamp())
        .withColumn("_source_file", lit("orders.csv"))
    )