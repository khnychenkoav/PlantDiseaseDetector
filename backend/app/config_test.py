import os
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env.test")

class ConfigTestSetup(BaseSettings):
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

config_test_setup = ConfigTestSetup()

def get_test_db_url() -> str:
    """Возвращает URL для подключения к тестовой базе данных."""
    return (
        f"postgresql+asyncpg://{config_test_setup.DB_USER}:{config_test_setup.DB_PASSWORD}@"
        f"{config_test_setup.DB_HOST}:{config_test_setup.DB_PORT}/{config_test_setup.DB_NAME}"
    )

def get_test_auth_data():
    return {"secret_key": config_test_setup.SECRET_KEY, "algorithm": config_test_setup.ALGORITHM}