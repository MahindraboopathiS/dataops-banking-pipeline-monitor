-- Row counts by table
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'accounts', COUNT(*) FROM accounts
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions
UNION ALL
SELECT 'quality_check_results', COUNT(*) FROM quality_check_results;

-- Latest event timestamp
SELECT MAX(event_timestamp) AS latest_event_timestamp
FROM transactions;

-- EXPLAIN example: booking-date operational query
EXPLAIN
SELECT booking_date, COUNT(*) AS transaction_count
FROM transactions
GROUP BY booking_date
ORDER BY booking_date;

-- EXPLAIN example: high-risk transaction query
EXPLAIN
SELECT *
FROM transactions
WHERE is_suspicious = TRUE
ORDER BY event_timestamp DESC
LIMIT 50;

-- Future optimization note:
-- For much larger volumes, partition transactions by booking_date and review indexes
-- on source_system, channel, status and is_suspicious according to workload patterns.
