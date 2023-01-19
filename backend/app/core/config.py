from pydantic import BaseSettings

class Base(BaseSettings):
    """Base configurations."""
    APPLICATION_NAME: str = "Asset Repository"
    APPLICATION_PORT: int = 5050
    API_VERSION: str = "v1"
    APPLICATION_ROOT_URL:str=f"/api/{API_VERSION}"
    DEBUG:bool=False