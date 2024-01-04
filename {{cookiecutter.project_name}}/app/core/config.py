from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    APP_NAME: str = "{{cookiecutter.project_name}}"
    APP_V1_STR: str = "/api/v1"
    # e.g:  [ "http://localhost","http://localhost:8000",]
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DATABASE_URL: str = "postgresql://postgres:123@localhost/fastapi"
    PORT: int = 8000
    # openssl rand -hex 32
    SECRET_KEY: str = "7b0d6d7aaed1d6f300533fd8448d54495a1d3ec3b362e95c7e0c62c7c88d69e8"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


setting = Setting()
