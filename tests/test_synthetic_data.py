from pathlib import Path

import pandas as pd

from banking_dataops.generate_synthetic_data import SyntheticConfig, generate


def test_generate_synthetic_data_files(tmp_path: Path) -> None:
    generate(SyntheticConfig(customers=3, accounts_per_customer=2, transactions=25), tmp_path)

    customers = tmp_path / "synthetic_customers.csv"
    accounts = tmp_path / "synthetic_accounts.csv"
    transactions = tmp_path / "synthetic_transactions.csv"

    assert customers.exists()
    assert accounts.exists()
    assert transactions.exists()

    assert len(pd.read_csv(customers)) == 3
    assert len(pd.read_csv(accounts)) == 6
    frame = pd.read_csv(transactions)
    assert len(frame) == 25

    expected_columns = {
        "transaction_id",
        "account_id",
        "source_system",
        "event_timestamp",
        "booking_date",
        "amount_chf",
        "currency",
        "channel",
        "merchant_category",
        "country",
        "risk_score",
        "status",
        "is_suspicious",
        "created_at",
    }
    assert expected_columns.issubset(frame.columns)
    assert set(frame["status"]).issubset({"posted", "pending", "rejected"})
