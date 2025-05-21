import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    B2_ENDPOINT: str
    B2_BUCKET_NAME: str
    B2_ACCESS_KEY: str
    B2_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


def get_b2_data():
    return {
        "b2_endpoint": settings.B2_ENDPOINT,
        "b2_bucket_name": settings.B2_BUCKET_NAME,
        "b2_access_key": settings.B2_ACCESS_KEY,
        "b2_secret_key": settings.B2_SECRET_KEY,
    }
