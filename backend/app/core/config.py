from pydantic import BaseSettings,PostgresDsn
from typing import Optional

class DatabaseSettings(BaseSettings):
    POSTGRES_DATABASE_URI: Optional[PostgresDsn] = None

class Base(DatabaseSettings):
    """Base configurations."""
    APPLICATION_NAME: str = "Asset Repository"
    APPLICATION_PORT: int = 5050
    API_VERSION: str = "v1"
    APPLICATION_ROOT_URL:str=f"/api/{API_VERSION}"
    DEBUG:bool=False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'



