-- Bronze layer: Ingest customer data from source
CREATE OR REFRESH MATERIALIZED VIEW bronze_customer
AS
SELECT * FROM samples.tpch.customer