import os
from typing import List
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core application settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # API service settings
    ALLOWED_ORIGINS: List[str] = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

    # Add "testserver" for testing environments
    _allowed_hosts = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if os.getenv("TESTING", "False").lower() in ("true", "1", "t"):
        _allowed_hosts.append("testserver")
    ALLOWED_HOSTS: List[str] = _allowed_hosts

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()