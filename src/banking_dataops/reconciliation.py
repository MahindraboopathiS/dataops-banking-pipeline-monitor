"""Reconciliation summaries for synthetic regulated-data flows."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4

import pandas as pd

from banking_dataops.config import Settings, load_settings
from banking_dataops.db import connect, fetch_dataframe


@dataclass(frozen=True)
class SourceSystemSummary:
    """Source-system reconciliation summary."""

    source_system: str
    transaction_count: int
    total_amount_chf: Decimal


SOURCE_SYSTEM_QUERY = """
SELECT
    source_system,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_chf), 2) AS total_amount_chf,
    MIN(event_timestamp) AS first_event_timestamp,
    MAX(event_timestamp) AS last_event_timestamp
FROM transactions
GROUP BY source_system
ORDER BY source_system
"""

DAILY_RECONCILIATION_QUERY = """
SELECT
    booking_date,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_chf), 2) AS total_amount_chf,
    COUNT(*) FILTER (WHERE is_suspicious) AS suspicious_count
FROM transactions
GROUP BY booking_date
ORDER BY booking_date
"""

CHANNEL_SUMMARY_QUERY = """
SELECT
    channel,
    COUNT(*) AS transaction_count,
    ROUND(AVG(risk_score), 4) AS avg_risk_score,
    COUNT(*) FILTER (WHERE status <> 'posted') AS non_posted_count
FROM transactions
GROUP BY channel
ORDER BY transaction_count DESC
"""

STATUS_SUMMARY_QUERY = """
SELECT
    status,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_chf), 2) AS total_amount_chf
FROM transactions
GROUP BY status
ORDER BY status
"""

SUSPICIOUS_SUMMARY_QUERY = """
SELECT
    is_suspicious,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_chf), 2) AS total_amount_chf,
    ROUND(AVG(risk_score), 4) AS avg_risk_score
FROM transactions
GROUP BY is_suspicious
ORDER BY is_suspicious DESC
"""


def source_system_summary(settings: Settings | None = None) -> list[SourceSystemSummary]:
    """Return transaction counts and totals by source system."""

    frame = fetch_dataframe(SOURCE_SYSTEM_QUERY, settings=settings)
    return [
        SourceSystemSummary(
            source_system=str(row["source_system"]),
            transaction_count=int(row["transaction_count"]),
            total_amount_chf=Decimal(str(row["total_amount_chf"])),
        )
        for _, row in frame.iterrows()
    ]


def run_reconciliation(settings: Settings | None = None) -> dict[str, pd.DataFrame]:
    """Run all reconciliation summaries and persist a global count/amount summary."""

    runtime = settings or load_settings()
    summaries = {
        "source_system": fetch_dataframe(SOURCE_SYSTEM_QUERY, runtime),
        "daily": fetch_dataframe(DAILY_RECONCILIATION_QUERY, runtime),
        "channel": fetch_dataframe(CHANNEL_SUMMARY_QUERY, runtime),
        "status": fetch_dataframe(STATUS_SUMMARY_QUERY, runtime),
        "suspicious": fetch_dataframe(SUSPICIOUS_SUMMARY_QUERY, runtime),
    }

    total_count = int(summaries["source_system"]["transaction_count"].sum())
    total_amount = Decimal(str(summaries["source_system"]["total_amount_chf"].sum()))

    with connect(runtime) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO reconciliation_results
                    (reconciliation_id, reconciliation_name, source_count, target_count,
                     count_delta, source_total, target_total, amount_delta)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    f"REC-{uuid4().hex[:12].upper()}",
                    "source_system_total",
                    total_count,
                    total_count,
                    0,
                    total_amount,
                    total_amount,
                    Decimal("0.00"),
                ),
            )
        connection.commit()

    return summaries


def print_reconciliation_summary(summary: dict[str, pd.DataFrame]) -> None:
    """Print a CLI-friendly reconciliation summary."""

    for name, frame in summary.items():
        print(f"\n## {name}")
        print(frame.to_string(index=False))


def main() -> None:
    """CLI entry point."""

    print_reconciliation_summary(run_reconciliation())


if __name__ == "__main__":
    main()
