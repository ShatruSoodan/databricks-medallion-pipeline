# Databricks notebook source
import dlt
from pyspark.sql.functions import current_timestamp, lit

@dlt.table(
    name="bronze_products",
    comment="Raw product data ingested from CSV with audit columns",
    table_properties={
        "quality": "bronze",
        "pipelines.autoOptimize.managed": "true"
    }
)
def bronze_products():
    """
    Ingest raw product data from CSV files in Unity Catalog volume.
    Adds audit columns: _ingestion_timestamp and _source_file.
    """
    return (
        spark.read
        .format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load("/Volumes/workspace/dev/medallion_data/products.csv")
        .withColumn("_ingestion_timestamp", current_timestamp())
        .withColumn("_source_file", lit("products.csv"))
    )