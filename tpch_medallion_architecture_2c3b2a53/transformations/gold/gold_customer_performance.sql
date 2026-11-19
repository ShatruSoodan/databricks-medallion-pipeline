-- Gold layer: Customer performance metrics
CREATE OR REFRESH MATERIALIZED VIEW gold_customer_performance
AS
SELECT 
  c.c_custkey,
  c.c_name,
  c.nation_name,
  c.region_name,
  COUNT(DISTINCT o.o_orderkey) AS order_count,
  SUM(o.l_extendedprice * (1 - o.l_discount)) AS total_revenue,
  AVG(o.l_discount) AS avg_discount,
  AVG(o.l_extendedprice) AS avg_extended_price
FROM silver_customers c
LEFT JOIN silver_orders o ON c.c_custkey = o.o_custkey
GROUP BY ALL