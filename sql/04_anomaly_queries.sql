-- High-risk transactions
SELECT *
FROM transactions
WHERE risk_score > 0.85
ORDER BY risk_score DESC
LIMIT 100;

-- High-amount transactions
SELECT *
FROM transactions
WHERE amount_chf > 50000
ORDER BY amount_chf DESC
LIMIT 100;

-- Account daily velocity
SELECT account_id, booking_date, COUNT(*) AS transaction_count
FROM transactions
GROUP BY account_id, booking_date
HAVING COUNT(*) > 10
ORDER BY transaction_count DESC;

-- Rejected transactions by channel
SELECT channel, COUNT(*) AS rejected_count
FROM transactions
WHERE status = 'rejected'
GROUP BY channel
ORDER BY rejected_count DESC;

-- Suspicious transactions by country
SELECT country, COUNT(*) AS suspicious_count, ROUND(AVG(risk_score), 4) AS avg_risk_score
FROM transactions
WHERE is_suspicious
GROUP BY country
ORDER BY suspicious_count DESC;
