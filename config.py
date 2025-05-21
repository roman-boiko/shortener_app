from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    env_name: str = "local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shoterner.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    print(f"Environment: {settings.env_name}")
    print(f"Base URL: {settings.base_url}")
    print(f"Database URL: {settings.db_url}")
    return settings
