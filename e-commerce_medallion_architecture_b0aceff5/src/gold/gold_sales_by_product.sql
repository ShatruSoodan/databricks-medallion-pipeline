-- Gold Layer: Sales metrics by product
-- Aggregates from quality-passed silver data only

CREATE OR REFRESH MATERIALIZED VIEW workspace.dev.gold_sales_by_product
AS
SELECT 
  p.product_id,
  p.product_name,
  p.category,
  COUNT(DISTINCT o.order_id) AS total_orders,
  SUM(o.total_amount) AS total_revenue,
  AVG(o.total_amount) AS avg_order_value
FROM workspace.dev.silver_products p
LEFT JOIN workspace.dev.silver_orders o 
  ON p.product_id = o.product_id 
  AND o.quality_check_passed = true
WHERE p.quality_check_passed = true
GROUP BY ALL
ORDER BY total_revenue DESC