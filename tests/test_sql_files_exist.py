from pathlib import Path


def test_required_sql_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        "00_schema.sql",
        "01_seed_reference_data.sql",
        "02_data_quality_checks.sql",
        "03_reconciliation_queries.sql",
        "04_anomaly_queries.sql",
        "05_performance_queries.sql",
    ]

    for filename in required:
        path = root / "sql" / filename
        assert path.exists(), f"Missing {filename}"
        assert path.read_text(encoding="utf-8").strip(), f"Empty {filename}"
