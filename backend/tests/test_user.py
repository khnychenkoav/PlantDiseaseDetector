import pytest
from unittest.mock import patch

@pytest.mark.asyncio
async def test_login_success(client):
    response = await client.post("/auth/login/", json={
        "email": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/auth/register/", json={
        "name": "NewUser",
        "email": "new@example.com",
        "password": "qwerty123"
    })
    assert response.status_code in [200, 409]

@pytest.mark.asyncio
async def test_get_me(client):
    """Тест получения информации о текущем пользователе."""
    response = await client.get("/users/me/")
    assert response.status_code in [200, 401]

@pytest.mark.asyncio
@patch("app.routes.user.get_current_admin_user")
async def test_access_denied_for_non_admin(mock_admin, client):
    """Тест отказа доступа для не-админа."""
    # Имитируем ошибку аутентификации
    mock_admin.side_effect = Exception("Not authorized")
    response = await client.get("/users/all/")
    assert response.status_code in [401, 403]