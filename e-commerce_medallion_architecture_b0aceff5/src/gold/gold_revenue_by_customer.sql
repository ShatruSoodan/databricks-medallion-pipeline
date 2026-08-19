-- Gold Layer: Revenue metrics by customer
-- Aggregates from quality-passed silver data only

CREATE OR REFRESH MATERIALIZED VIEW workspace.dev.gold_revenue_by_customer
AS
SELECT 
  c.customer_id,
  c.customer_name,
  c.customer_segment,
  COUNT(DISTINCT o.order_id) AS total_orders,
  COALESCE(SUM(o.total_amount), 0) AS total_revenue,
  AVG(o.total_amount) AS avg_order_value,
  c.lifetime_value AS lifetime_value_actual
FROM workspace.dev.silver_customers c
LEFT JOIN workspace.dev.silver_orders o 
  ON c.customer_id = o.customer_id 
  AND o.quality_check_passed = true
WHERE c.quality_check_passed = true
GROUP BY ALL
ORDER BY total_revenue DESC