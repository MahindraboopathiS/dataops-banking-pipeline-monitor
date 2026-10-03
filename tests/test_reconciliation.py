from banking_dataops.reconciliation import (
    CHANNEL_SUMMARY_QUERY,
    DAILY_RECONCILIATION_QUERY,
    SOURCE_SYSTEM_QUERY,
    STATUS_SUMMARY_QUERY,
    SUSPICIOUS_SUMMARY_QUERY,
    SourceSystemSummary,
)


def test_reconciliation_queries_exist() -> None:
    for query in [
        SOURCE_SYSTEM_QUERY,
        DAILY_RECONCILIATION_QUERY,
        CHANNEL_SUMMARY_QUERY,
        STATUS_SUMMARY_QUERY,
        SUSPICIOUS_SUMMARY_QUERY,
    ]:
        assert "SELECT" in query.upper()
        assert "transactions" in query.lower()


def test_source_system_summary_shape() -> None:
    row = SourceSystemSummary("core_banking", 10, 1234)
    assert row.source_system == "core_banking"
    assert row.transaction_count == 10
