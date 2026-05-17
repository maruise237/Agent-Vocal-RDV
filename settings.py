from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    dashboard_password: str = "change-me"
    airtable_api_key: str | None = None
    airtable_base_id: str | None = None
    airtable_appointments_table: str = "Rendez-vous"
    airtable_config_table: str = "Config"
    google_service_account_json: str | None = None
    google_calendar_id: str = "primary"
    google_calendar_timezone: str = "Africa/Douala"
    company_name: str = "KamTech"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
