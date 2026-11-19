-- Bronze layer: Ingest orders data from source
CREATE OR REFRESH MATERIALIZED VIEW bronze_orders
AS
SELECT * FROM samples.tpch.orders