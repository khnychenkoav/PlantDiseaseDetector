import os
import sys
import asyncio
import uuid
from typing import AsyncGenerator
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

# --- Добавление пути для импортов ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# --- Импорты приложения ---
from main import app
from app.repository.repository import get_async_session, Base
from app.repository.models import User as UserModel, Disease as DiseaseModel
from app.dao.user import UserDAO
from app.dao.disease import DiseaseDAO

# --- Импорт тестовой конфигурации ---
from app.config_test import get_test_db_url

# --- Настройка тестовой БД ---
TEST_DATABASE_URL = get_test_db_url()

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --- Monkeypatching Фабрики Сессий в DAO ---
@pytest.fixture(scope='session', autouse=True)
def patch_dao_session_factory():
    """
    Подменяет фабрику сессий `async_session_maker` во всех указанных DAO модулях
    на тестовую фабрику `TestingSessionLocal` на время всей тестовой сессии.
    Это гарантирует, что DAO будут работать с тестовой базой данных.
    """
    patch_targets = [
        'app.dao.history.async_session_maker',
        'app.dao.user.async_session_maker',
        'app.dao.disease.async_session_maker',
    ]
    patchers = [patch(target, TestingSessionLocal) for target in patch_targets]
    successful_patches = 0
    for p in patchers:
        try:
            p.start()
            successful_patches += 1
        except (AttributeError, ModuleNotFoundError):
            # Игнорируем ошибки, если путь к фабрике в каком-то DAO указан неверно
            # или DAO не использует фабрику таким образом.
            pass
    yield # Тесты выполняются здесь
    for p in patchers:
        try:
            if p.is_local:
                 p.stop()
        except RuntimeError:
             pass

# --- Фикстура цикла событий (Session-Scoped) ---
@pytest.fixture(scope="session")
def event_loop():
    """Создает экземпляр цикла событий по умолчанию для тестовой сессии."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# --- Очистка БД перед каждым тестом ---
@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """
    Гарантирует чистую базу данных перед каждым тестом.
    Удаляет все таблицы и создает их заново.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# --- Переопределение зависимости FastAPI для сессии ---
@pytest_asyncio.fixture(scope="function", autouse=True)
async def override_dependency():
    """
    Переопределяет зависимость `get_async_session` в FastAPI.
    Заставляет FastAPI использовать сессии из `TestingSessionLocal` для каждого запроса.
    """
    async def override_get_async_session_for_test() -> AsyncGenerator[AsyncSession, None]:
         async with TestingSessionLocal() as session:
              yield session

    original_override = app.dependency_overrides.get(get_async_session)
    app.dependency_overrides[get_async_session] = override_get_async_session_for_test
    yield
    # Восстанавливаем исходное состояние после теста
    if original_override:
        app.dependency_overrides[get_async_session] = original_override
    else:
        app.dependency_overrides.pop(get_async_session, None)


# --- Базовый HTTP Клиент ---
@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Предоставляет базовый асинхронный HTTP клиент для выполнения запросов к приложению."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

# --- Фикстуры данных (используют DAO с подмененной сессией) ---

@pytest_asyncio.fixture(scope="function")
async def test_user() -> UserModel:
    """
    Создает и возвращает тестового пользователя в БД через UserDAO.
    Предполагается, что UserDAO.create_user использует подмененную сессию
    и выполняет commit/refresh.
    """
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user = await UserDAO.create_user(
        name="Test User",
        email=unique_email,
        password="password" # Используется для логина в других фикстурах/тестах
    )
    return user

@pytest_asyncio.fixture(scope="function")
async def test_admin_user(db_session: AsyncSession) -> UserModel:
    """
    Создает тестового пользователя через UserDAO, затем явно устанавливает
    флаг is_admin=True и сохраняет его через сессию теста (`db_session`).
    Возвращает пользователя с установленным флагом администратора.
    """
    unique_email = f"admin_{uuid.uuid4()}@example.com"
    admin = await UserDAO.create_user(
        name="Admin User",
        email=unique_email,
        password="password" # Используется для логина в других фикстурах/тестах
    )
    # Явно устанавливаем флаг админа и сохраняем через сессию теста
    admin.is_admin = True
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin

@pytest_asyncio.fixture(scope="function")
async def test_disease() -> DiseaseModel:
    """
    Создает и возвращает тестовую болезнь в БД через DiseaseDAO.
    Предполагается, что DiseaseDAO.create_record использует подмененную сессию
    и выполняет commit/refresh.
    """
    disease_name = f"Тестовая болезнь {uuid.uuid4()}"
    disease_reason = "Тестовая причина"
    disease_recommendation = "Тестовая рекомендация"
    # Передаем аргументы раздельно, как ожидается DAO
    disease = await DiseaseDAO.create_record(
        name=disease_name,
        reason=disease_reason,
        recommendation=disease_recommendation
    )
    return disease

# --- Фикстуры аутентифицированного клиента ---

@pytest_asyncio.fixture(scope="function")
async def authenticated_client(client: AsyncClient, test_user: UserModel) -> AsyncClient:
    """
    Выполняет вход пользователя `test_user` и возвращает
    HTTP клиент с установленными данными аутентификации (если API их использует).
    """
    login_data = {"email": test_user.email, "password": "password"}
    response = await client.post("/auth/login/", json=login_data)
    assert response.status_code == 200, f"Login failed for {test_user.email}: {response.text}"
    token = response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest_asyncio.fixture(scope="function")
async def authenticated_admin_client(client: AsyncClient, test_admin_user: UserModel) -> AsyncClient:
    """
    Выполняет вход пользователя `test_admin_user` и возвращает
    HTTP клиент с установленными данными аутентификации (если API их использует).
    """
    login_data = {"email": test_admin_user.email, "password": "password"}
    response = await client.post("/auth/login/", json=login_data)
    assert response.status_code == 200, f"Admin login failed for {test_admin_user.email}: {response.text}"
    token = response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

# --- Опциональная фикстура сессии для прямых проверок в тестах ---
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Предоставляет экземпляр тестовой сессии (`AsyncSession`) напрямую в тест.
    Полезно для выполнения прямых запросов к БД или проверок состояния
    независимо от кода приложения/DAO.
    """
    async with TestingSessionLocal() as session:
        yield session
