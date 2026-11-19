-- Bronze layer: Ingest lineitem data from source
CREATE OR REFRESH MATERIALIZED VIEW bronze_lineitem
AS
SELECT * FROM samples.tpch.lineitem