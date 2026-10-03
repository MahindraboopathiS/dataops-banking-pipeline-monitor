-- Source-system reconciliation
SELECT
    source_system,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_chf), 2) AS total_amount_chf,
    MIN(event_timestamp) AS first_event_timestamp,
    MAX(event_timestamp) AS last_event_timestamp
FROM transactions
GROUP BY source_system
ORDER BY source_system;

-- Daily booking reconciliation
SELECT
    booking_date,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_chf), 2) AS total_amount_chf,
    COUNT(*) FILTER (WHERE is_suspicious) AS suspicious_count
FROM transactions
GROUP BY booking_date
ORDER BY booking_date;

-- Channel summary
SELECT
    channel,
    COUNT(*) AS transaction_count,
    ROUND(AVG(risk_score), 4) AS avg_risk_score,
    COUNT(*) FILTER (WHERE status <> 'posted') AS non_posted_count
FROM transactions
GROUP BY channel
ORDER BY transaction_count DESC;

-- Status summary
SELECT
    status,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_chf), 2) AS total_amount_chf
FROM transactions
GROUP BY status
ORDER BY status;

-- Suspicious summary
SELECT
    is_suspicious,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_chf), 2) AS total_amount_chf,
    ROUND(AVG(risk_score), 4) AS avg_risk_score
FROM transactions
GROUP BY is_suspicious
ORDER BY is_suspicious DESC;
