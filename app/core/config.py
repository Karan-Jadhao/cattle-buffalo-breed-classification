from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    supabase_url: str
    supabase_service_key: str
    model_path: str = "DL/models/cattle_breed_model.pth"
    frontend_url: str = "http://localhost:5173"

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
