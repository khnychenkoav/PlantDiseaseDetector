import os
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env.test")

class TestSettings(BaseSettings):
    """
    Настройки для тестовой среды.
    Загружает переменные из файла .env.test или из переменных окружения.
    """
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str = "test_secret"
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=dotenv_path,
        extra='ignore'
    )

test_settings = TestSettings()

def get_test_db_url() -> str:
    """Возвращает URL для подключения к тестовой базе данных."""
    return (
        f"postgresql+asyncpg://{test_settings.DB_USER}:{test_settings.DB_PASSWORD}@"
        f"{test_settings.DB_HOST}:{test_settings.DB_PORT}/{test_settings.DB_NAME}"
    )

def get_test_auth_data():
    return {"secret_key": test_settings.SECRET_KEY, "algorithm": test_settings.ALGORITHM}