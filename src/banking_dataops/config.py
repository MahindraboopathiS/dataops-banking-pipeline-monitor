"""Runtime configuration for the Banking DataOps Monitoring project."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Local runtime settings loaded from environment variables or `.env`."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_host: str = Field(default="localhost", validation_alias="BANKING_DATAOPS_DB_HOST")
    database_port: int = Field(default=5432, validation_alias="BANKING_DATAOPS_DB_PORT")
    database_name: str = Field(default="banking_dataops", validation_alias="BANKING_DATAOPS_DB_NAME")
    database_user: str = Field(default="dataops", validation_alias="BANKING_DATAOPS_DB_USER")
    database_password: str = Field(
        default="dataops_local_only",
        validation_alias="BANKING_DATAOPS_DB_PASSWORD",
    )
    data_dir: Path = Field(default=Path("data"), validation_alias="BANKING_DATAOPS_DATA_DIR")
    output_dir: Path = Field(default=Path("output"), validation_alias="BANKING_DATAOPS_OUTPUT_DIR")

    @property
    def dsn(self) -> str:
        """Return a psycopg-compatible DSN string for local PostgreSQL."""

        return (
            f"host={self.database_host} port={self.database_port} "
            f"dbname={self.database_name} user={self.database_user} "
            f"password={self.database_password}"
        )


def load_settings() -> Settings:
    """Load runtime settings."""

    return Settings()


# Backward-compatible aliases for earlier starter files/tests.
DatabaseConfig = Settings
load_database_config = load_settings
