import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/auth/register/", json={
        "name": "NewUser",
        "email": "new@example.com",
        "password": "qwerty123"
    })
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_success(client):
    response = await client.post("/auth/login/", json={
        "email": "new@example.com",
        "password": "qwerty123"
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """Тест входа с неверными учетными данными."""
    response = await client.post("/auth/login/", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(client):
    """Тест выхода из системы."""
    response = await client.post("/users/logout/")
    assert response.status_code == 200