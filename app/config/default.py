import os
from typing import Dict

from dotenv import load_dotenv
from pydantic import BaseSettings

# Загружаем переменные окружения для базы
load_dotenv()


class AppSettings(BaseSettings):
    """
    Default config for application.
    """

    PATH_PREFIX: str = os.environ.get("PATH_PREFIX", "")

    APP_HOST: str = os.environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(os.environ.get("APP_PORT", 8080))

    DATABASE_NAME: str = os.environ.get("POSTGRES_DB", "database")
    DATABASE_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
    DATABASE_USERNAME: str = os.environ.get("POSTGRES_USER", "user")
    DATABASE_PORT: int = int(os.environ.get("POSTGRES_PORT", "5432")[-4:])
    DATABASE_PASSWORD: str = os.environ.get(
        "POSTGRES_PASSWORD", "user_password"
    )

    @property
    def database_settings(self) -> Dict[str, str or int]:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.DATABASE_NAME,
            "user": self.DATABASE_USERNAME,
            "password": self.DATABASE_PASSWORD,
            "host": self.DATABASE_HOST,
            "port": self.DATABASE_PORT,
        }

    @property
    def database_uri_async(self) -> str:
        """
        Get sync uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get async uri for connection with database.
        """
        return (
            "postgresql://{user}:{password}@{host}:{port}/{database}".format(
                **self.database_settings,
            )
        )
