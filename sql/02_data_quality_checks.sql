-- CTRL-001 critical_nulls
SELECT 'critical_nulls' AS check_name, COUNT(*) AS failed_rows
FROM transactions
WHERE transaction_id IS NULL
   OR account_id IS NULL
   OR event_timestamp IS NULL
   OR amount_chf IS NULL;

-- CTRL-002 duplicate_transactions
SELECT 'duplicate_transactions' AS check_name, COUNT(*) AS failed_rows
FROM (
    SELECT transaction_id
    FROM transactions
    GROUP BY transaction_id
    HAVING COUNT(*) > 1
) duplicates;

-- CTRL-003 invalid_amounts
SELECT 'invalid_amounts' AS check_name, COUNT(*) AS failed_rows
FROM transactions
WHERE amount_chf <= 0
   OR amount_chf > 1000000;

-- CTRL-004 orphan_transactions
SELECT 'orphan_transactions' AS check_name, COUNT(*) AS failed_rows
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;

-- CTRL-005 invalid_risk_score
SELECT 'invalid_risk_score' AS check_name, COUNT(*) AS failed_rows
FROM transactions
WHERE risk_score < 0
   OR risk_score > 1;

-- CTRL-006 invalid_status
SELECT 'invalid_status' AS check_name, COUNT(*) AS failed_rows
FROM transactions
WHERE status NOT IN ('posted', 'pending', 'rejected');

-- CTRL-007 stale_data
SELECT 'stale_data' AS check_name,
       CASE
           WHEN MAX(event_timestamp) < CURRENT_TIMESTAMP - INTERVAL '60 days'
           THEN 1
           ELSE 0
       END AS failed_rows
FROM transactions;
