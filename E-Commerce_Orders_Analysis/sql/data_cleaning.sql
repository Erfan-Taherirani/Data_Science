-- Duplicate Detection

/*
    data contains 125 exact duplicates.
*/
-- SELECT
--     *
-- FROM (
--     SELECT
--         order_id,
--         ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_id) as dup_flag
--     FROM orders
-- ) t
-- WHERE dup_flag > 1;

-- Deduplication Task
WITH CTE_deduplicate_table AS (
    SELECT DISTINCT *
    FROM orders
)

SELECT
    order_date,
    CASE
        WHEN order_date IS NULL THEN 1
        ELSE 0
    END AS is_null
FROM CTE_deduplicate_table