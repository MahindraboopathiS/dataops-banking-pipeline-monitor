# Data Dictionary — banking-dataops-monitoring

## customers

| Column | Type | Description | Quality rule |
|---|---|---|---|
| customer_id | TEXT | Synthetic customer identifier | Required, unique |
| customer_segment | TEXT | Synthetic segment: retail, premium, sme | Required |
| country | TEXT | Synthetic domicile country | Required |
| created_at | TIMESTAMP | Synthetic creation timestamp | Required |

## accounts

| Column | Type | Description | Quality rule |
|---|---|---|---|
| account_id | TEXT | Synthetic account identifier | Required, unique |
| customer_id | TEXT | Related synthetic customer | Required, must exist in customers |
| account_type | TEXT | Synthetic account type | Required |
| currency | TEXT | Account currency | Required |
| opened_at | TIMESTAMP | Synthetic opening timestamp | Required |

## transactions

| Column | Type | Description | Quality rule |
|---|---|---|---|
| transaction_id | TEXT | Synthetic transaction identifier | Required, unique |
| account_id | TEXT | Related synthetic account | Required, must exist in accounts |
| source_system | TEXT | Synthetic source feed | Required |
| event_timestamp | TIMESTAMP | Event timestamp | Required |
| booking_date | DATE | Booking date | Required |
| amount_chf | NUMERIC | Synthetic amount in CHF | Required, > 0, <= 1,000,000 |
| currency | TEXT | Transaction currency | Required |
| channel | TEXT | Source channel | Required |
| merchant_category | TEXT | Synthetic merchant category | Required |
| country | TEXT | Synthetic transaction country | Required |
| risk_score | NUMERIC | Synthetic risk score | Required, 0-1 |
| status | TEXT | Synthetic transaction status | Required |
| is_suspicious | BOOLEAN | Synthetic anomaly flag | Required |
| created_at | TIMESTAMP | Load timestamp | Required |

## quality_check_results

| Column | Type | Description |
|---|---|---|
| check_id | TEXT | Control identifier |
| control_id | TEXT | Control ID |
| check_name | TEXT | Control name |
| status | TEXT | PASS, WARN or FAIL |
| failed_rows | INTEGER | Failed row count |
| severity | TEXT | high, medium or low |
| executed_at | TIMESTAMP | Execution timestamp |

## reconciliation_results

| Column | Type | Description |
|---|---|---|
| reconciliation_id | TEXT | Synthetic result identifier |
| reconciliation_name | TEXT | Reconciliation type |
| source_count | INTEGER | Source count |
| target_count | INTEGER | Target count |
| count_delta | INTEGER | Count difference |
| source_total | NUMERIC | Source amount |
| target_total | NUMERIC | Target amount |
| amount_delta | NUMERIC | Amount difference |
| executed_at | TIMESTAMP | Execution timestamp |

## Public-safety note

All data is synthetic. No real banking, insurance, health, client, employer or private data should be stored here.
