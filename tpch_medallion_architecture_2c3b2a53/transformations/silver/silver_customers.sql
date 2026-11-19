-- Silver layer: Enrich customers with nation and region details
CREATE OR REFRESH MATERIALIZED VIEW silver_customers
AS
SELECT 
  c.c_custkey,
  c.c_name,
  c.c_address,
  c.c_nationkey,
  c.c_phone,
  c.c_acctbal,
  c.c_mktsegment,
  c.c_comment,
  n.n_name AS nation_name,
  r.r_name AS region_name
FROM bronze_customer c
INNER JOIN samples.tpch.nation n ON c.c_nationkey = n.n_nationkey
INNER JOIN samples.tpch.region r ON n.n_regionkey = r.r_regionkey