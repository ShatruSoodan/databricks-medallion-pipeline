-- Silver layer: Enrich orders with lineitem details
CREATE OR REFRESH MATERIALIZED VIEW silver_orders
(
  CONSTRAINT valid_ship_date EXPECT (l_shipdate >= o_orderdate) ON VIOLATION DROP ROW
)
AS
SELECT 
  o.o_orderkey,
  o.o_custkey,
  o.o_orderstatus,
  o.o_totalprice,
  o.o_orderdate,
  o.o_orderpriority,
  o.o_clerk,
  o.o_shippriority,
  o.o_comment,
  l.l_extendedprice,
  l.l_discount,
  l.l_shipdate
FROM bronze_orders o
INNER JOIN bronze_lineitem l ON o.o_orderkey = l.l_orderkey