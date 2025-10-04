from typing import List
import os

class Settings:
    """
    Application settings, loaded from environment variables.
    """
    # It is recommended to set these in your environment for production.
    # The default values are for development purposes.
    ALLOWED_ORIGINS: List[str] = os.environ.get(
        "ALLOWED_ORIGINS",
        "http://localhost,http://localhost:3000,http://localhost:8000,https://your-frontend-domain.com"
    ).split(",")

    ALLOWED_HOSTS: List[str] = os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1,your-api-domain.com"
    ).split(",")

    DEBUG: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

settings = Settings()