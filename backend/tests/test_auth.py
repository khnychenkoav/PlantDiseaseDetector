import pytest
from httpx import AsyncClient
from app.repository.models import User # Используется для аннотации типа test_user

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    """Тестирует успешную регистрацию нового пользователя."""
    response = await client.post("/auth/register/", json={
        "name": "NewRegUser",
        "email": "newreg@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newreg@example.com"
    assert data["name"] == "NewRegUser"
    assert "password" not in data # Пароль не должен возвращаться

@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient, test_user: User):
    """Тестирует невозможность регистрации пользователя с уже существующим email."""
    response = await client.post("/auth/register/", json={
        "name": "Another User",
        "email": test_user.email, # Используем email из фикстуры
        "password": "anotherpassword"
    })
    assert response.status_code == 409 # Conflict
    assert "Пользователь уже существует" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user: User):
    """Тестирует успешный вход существующего пользователя."""
    login_data = {"email": test_user.email, "password": "password"} # Пароль из фикстуры
    response = await client.post("/auth/login/", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data # Проверяем наличие токена

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: User):
    """Тестирует невозможность входа с неверным паролем."""
    login_data = {"email": test_user.email, "password": "wrongpassword"}
    response = await client.post("/auth/login/", json=login_data)
    assert response.status_code == 401 # Unauthorized
    assert "Неверная почта или пароль" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Тестирует невозможность входа несуществующего пользователя."""
    login_data = {"email": "nonexistent@example.com", "password": "password123"}
    response = await client.post("/auth/login/", json=login_data)
    assert response.status_code == 401 # Unauthorized
    assert "Неверная почта или пароль" in response.json()["detail"]

@pytest.mark.asyncio
async def test_logout(authenticated_client: AsyncClient):
    """Тестирует успешный выход пользователя из системы."""
    response = await authenticated_client.post("/users/logout/")
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь успешно вышел из системы"}

    # Проверяем, что защищенный эндпоинт недоступен после выхода
    response_after_logout = await authenticated_client.get("/users/me/")
    assert response_after_logout.status_code == 401 # Unauthorized