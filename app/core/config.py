import os
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLITE_DATABASE_URL", "sqlite:///./database.db"
    )


settings = Settings()
