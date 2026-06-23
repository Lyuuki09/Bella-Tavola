from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Bella Tavola API"
    app_version: str = "1.0.0"
    app_description: str = "API do restaurante Bella Tavola"
    debug: bool = False
    max_mesas: int = 20
    max_pessoas_por_mesa: int = 10
    model_repo_id: str = ""
    model_filename: str = "model.pkl"
    model_version: str = "local-dev"
    database_url: str = Field(
        default="sqlite:///./data/bella_tavola.db",
        description="String de conexao SQLAlchemy (PostgreSQL em producao, SQLite em testes locais).",
    )


settings = Settings()
