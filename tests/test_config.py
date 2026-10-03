from banking_dataops.config import Settings


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.database_host == "localhost"
    assert settings.database_port == 5432
    assert settings.database_name == "banking_dataops"
    assert "dbname=banking_dataops" in settings.dsn
    assert "user=dataops" in settings.dsn
