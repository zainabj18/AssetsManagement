from typing import Optional,Dict,Any,Union
from pydantic import BaseSettings,validator,PostgresDsn
from typing import Optional
import os
import secrets

class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: Optional[str]="5432"
    POSTGRES_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("POSTGRES_DATABASE_URI")
    def validate_db_uri(cls, v: Optional[str], values: Dict[str,Any]) -> PostgresDsn:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            port=values.get("POSTGRES_PORT"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB')}",
        )

class Base(DatabaseSettings):
    """Base configurations."""
    APPLICATION_NAME: str = "Asset Repository"
    APPLICATION_PORT: int = 5050
    API_VERSION: str = "v1"
    APPLICATION_ROOT_URL:str=f"/api/{API_VERSION}"
    DEBUG:bool=False
    DEFAULT_SUPERUSER_USERNAME:str='admin'
    DEFAULT_SUPERUSER_PASSWORD:str='admin'
    SECRET_KEY:str=secrets.token_urlsafe(16)
    JWT_ALGO:str="HS256"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class DevelopmentConfig(Base):
    """Development configurations."""
    ENV="development"
    DEBUG=True
    class Config:
        env_prefix: str = "DEV_"

class ProductionConfig(Base):
    """Production configurations."""
    DEBUG=False
    class Config:
        env_prefix: str = "PROD_"

class BaseTestConfig(Base):
    ENV="test"
    DEBUG=True

config=dict(DEV=DevelopmentConfig,PROD=ProductionConfig,TEST=BaseTestConfig)
settings: Union[DevelopmentConfig, ProductionConfig,BaseTestConfig] = config[os.environ.get('ENV_STATE', 'dev').upper()]()
