-- Gold Layer: Customer segmentation analysis
-- Segments customers based on order behavior and revenue
-- Rules: High-Value (>$10K revenue), Repeat (5+ orders), One-Time (1 order), Inactive (no orders in 180 days)

CREATE OR REFRESH MATERIALIZED VIEW workspace.dev.gold_customer_segmentation
AS
WITH customer_stats AS (
  SELECT 
    c.customer_id,
    COUNT(DISTINCT o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_revenue,
    MAX(o.order_date) AS last_order_date,
    DATEDIFF(CURRENT_DATE(), MAX(o.order_date)) AS days_since_last_order
  FROM workspace.dev.silver_customers c
  LEFT JOIN workspace.dev.silver_orders o 
    ON c.customer_id = o.customer_id 
    AND o.quality_check_passed = true
  WHERE c.quality_check_passed = true
  GROUP BY c.customer_id
),
customer_segments AS (
  SELECT 
    customer_id,
    CASE 
      WHEN total_revenue > 10000 THEN 'High-Value'
      WHEN order_count >= 5 THEN 'Repeat'
      WHEN order_count = 1 THEN 'One-Time'
      WHEN days_since_last_order > 180 OR last_order_date IS NULL THEN 'Inactive'
      ELSE 'Regular'
    END AS segment_type,
    total_revenue
  FROM customer_stats
)
SELECT 
  segment_type,
  COUNT(customer_id) AS customer_count,
  ROUND(AVG(total_revenue), 2) AS avg_revenue,
  SUM(total_revenue) AS total_revenue
FROM customer_segments
GROUP BY segment_type
ORDER BY total_revenue DESC