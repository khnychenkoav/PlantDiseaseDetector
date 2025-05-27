import pytest
import uuid
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.models import User as UserModel

@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    """Тестирует невозможность получения данных о себе неаутентифицированным пользователем."""
    response = await client.get("/users/me/")
    assert response.status_code == 401 # Unauthorized

@pytest.mark.asyncio
async def test_get_me_authorized(authenticated_client: AsyncClient, test_user: UserModel):
    """Тестирует успешное получение данных о себе аутентифицированным пользователем."""
    response = await authenticated_client.get("/users/me/")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name
    assert data["id"] == str(test_user.id)
    assert data["is_user"] == test_user.is_user
    assert data["is_admin"] == test_user.is_admin
    assert data["is_super_admin"] == test_user.is_super_admin

@pytest.mark.asyncio
async def test_get_all_users_unauthorized(client: AsyncClient):
    """Тестирует невозможность получения списка всех пользователей неаутентифицированным пользователем."""
    response = await client.get("/users/all/")
    assert response.status_code == 401 # Unauthorized

@pytest.mark.asyncio
async def test_get_all_users_not_admin(authenticated_client: AsyncClient):
    """Тестирует невозможность получения списка всех пользователей обычным (не админ) пользователем."""
    response = await authenticated_client.get("/users/all/")
    assert response.status_code == 403 # Forbidden

@pytest.mark.asyncio
async def test_get_all_users_admin(authenticated_admin_client: AsyncClient, test_user: UserModel, test_admin_user: UserModel):
    """Тестирует успешное получение списка всех пользователей администратором."""
    response = await authenticated_admin_client.get("/users/all/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2 # Должны присутствовать как минимум тестовый юзер и админ
    emails = [user["email"] for user in data]
    assert test_user.email in emails
    assert test_admin_user.email in emails

@pytest.mark.asyncio
async def test_change_role_unauthorized(client: AsyncClient, test_user: UserModel):
    """Тестирует невозможность изменения роли неаутентифицированным пользователем."""
    response = await client.put("/users/change_role/", json={
        "email": test_user.email, # Используем email для идентификации
        "is_admin": True
    })
    assert response.status_code == 401 # Unauthorized

@pytest.mark.asyncio
async def test_change_role_not_admin(authenticated_client: AsyncClient, test_user: UserModel):
    """Тестирует невозможность изменения роли обычным (не админ) пользователем."""
    response = await authenticated_client.put("/users/change_role/", json={
        "email": test_user.email, # Используем email для идентификации
        "is_admin": True
    })
    assert response.status_code == 403 # Forbidden

@pytest.mark.asyncio
async def test_change_role_admin_success(
    authenticated_admin_client: AsyncClient,
    test_user: UserModel,
    db_session: AsyncSession
):
    """Тестирует успешное изменение роли пользователя администратором."""
    initial_admin_status = test_user.is_admin
    assert initial_admin_status is False

    # Отправляем запрос на изменение роли
    response = await authenticated_admin_client.put("/users/change_role/", json={
        "email": test_user.email, # Идентифицируем по email
        "is_admin": True          # Устанавливаем флаг админа
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Роль изменена"}

    # Проверяем изменение непосредственно в БД через сессию теста
    refreshed_user = await db_session.get(UserModel, test_user.id)
    assert refreshed_user is not None
    assert refreshed_user.is_admin is True # Флаг должен быть True

@pytest.mark.asyncio
async def test_change_role_admin_user_not_found(authenticated_admin_client: AsyncClient):
    """Тестирует попытку изменения роли для несуществующего пользователя администратором."""
    non_existent_email = f"not_found_{uuid.uuid4()}@example.com"
    response = await authenticated_admin_client.put("/users/change_role/", json={
        "email": non_existent_email, # Используем несуществующий email
        "is_admin": True
    })
    # API возвращает 409 Conflict, если пользователь не найден
    assert response.status_code == 409
    assert "Пользователь не найден" in response.json()["detail"]

@pytest.mark.asyncio
async def test_change_role_admin_invalid_data(authenticated_admin_client: AsyncClient, test_user: UserModel):
    """
    Тестирует попытку изменения роли с невалидными данными
    (например, неверный тип для флага is_admin). Ожидается ошибка валидации 422.
    """
    response = await authenticated_admin_client.put("/users/change_role/", json={
        "email": test_user.email,
        "is_admin": "не_булево" # Невалидное значение
    })
    assert response.status_code == 422 # Unprocessable Entity