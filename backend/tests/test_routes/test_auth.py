import pytest
import uuid
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
@pytest.mark.parametrize(
    "user_payload, expected_status_code, expected_detail_substring",
    [
        # Случай с дублирующимся email (используем email из фикстуры test_user)
        ({"name": "Another User", "email": "test_user_email_placeholder", "password": "anotherpassword"}, 409, "Пользователь уже существует"),
        # Невалидные данные (ожидаем 422 от FastAPI)
        ({"name": "Test", "email": "invalid", "password": "password123"}, 422, None),
        ({"name": "Test", "email": "", "password": "password123"}, 422, None), # Пустой email
        ({"name": "Test", "email": "valid@example.com", "password": ""}, 422, None), # Пустой пароль
        ({"name": "", "email": "valid2@example.com", "password": "password123"}, 422, None), # Пустое имя
        # Можно добавить другие сценарии, например, слишком короткий пароль, если у вас есть такая валидация
        # {"name": "Test", "email": "shortpass@example.com", "password": "123"}, 422, "Пароль слишком короткий"),
    ]
)
async def test_register_user_failure_scenarios(
    client: AsyncClient,
    test_user: User, # Нужна для сценария с дублирующимся email
    user_payload: dict,
    expected_status_code: int,
    expected_detail_substring: str | None,
):
    """
    Тестирует различные сценарии неудачной регистрации:
    - Дублирующийся email.
    - Невалидные данные (пустые поля, неверный формат email и т.д.).
    """
    # Если email в payload - это плейсхолдер, заменяем его на email из test_user
    if user_payload.get("email") == "test_user_email_placeholder":
        user_payload["email"] = test_user.email
    # Для других случаев, где email должен быть уникальным, но не дублировать test_user
    elif "email" in user_payload and expected_status_code != 409 : # Генерируем уникальный email для не-дублирующих тестов
        if not user_payload["email"] or user_payload["email"] == "invalid": # если email невалидный или пустой, не меняем
            pass
        else: # для валидных, но не дублирующих кейсов
            user_payload["email"] = f"test_failure_{uuid.uuid4()}@example.com"


    response = await client.post("/auth/register/", json=user_payload)

    assert response.status_code == expected_status_code
    if expected_detail_substring:
        assert expected_detail_substring in response.json()["detail"]
    elif expected_status_code == 422:
        assert "detail" in response.json()

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user: User):
    """Тестирует успешный вход существующего пользователя."""
    login_data = {"email": test_user.email, "password": "password"} # Пароль из фикстуры
    response = await client.post("/auth/login/", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data # Проверяем наличие токена

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "login_email, login_password, expected_status_code, expected_detail_substring",
    [
        ("test_user_email", "wrongpassword", 401, "Неверная почта или пароль"), # Используем test_user.email
        ("nonexistent@example.com", "password123", 401, "Неверная почта или пароль"),
        ("", "password123", 422, None), # Пустой email - ошибка валидации FastAPI
        ("test@example.com", "", 422, None), # Пустой пароль - ошибка валидации FastAPI
        ("notanemail", "password123", 422, None), # Невалидный формат email
    ]
)
async def test_login_failure_scenarios(
    client: AsyncClient,
    test_user: User, # Фикстура test_user нужна для сценария с правильным email, но неверным паролем
    login_email: str,
    login_password: str,
    expected_status_code: int,
    expected_detail_substring: str | None,
):
    """
    Тестирует различные сценарии неудачного входа:
    - Неверный пароль для существующего пользователя.
    - Несуществующий пользователь.
    - Невалидные данные (пустые поля, неверный формат email).
    """
    actual_email = test_user.email if login_email == "test_user_email" else login_email

    login_data = {"email": actual_email, "password": login_password}
    response = await client.post("/auth/login/", json=login_data)

    assert response.status_code == expected_status_code
    if expected_detail_substring:
        assert expected_detail_substring in response.json()["detail"]
    elif expected_status_code == 422: # Для ошибок валидации FastAPI
        # Проверяем, что в ответе есть поле "detail" (обычно это список ошибок)
        assert "detail" in response.json()

@pytest.mark.asyncio
async def test_logout(authenticated_client: AsyncClient):
    """Тестирует успешный выход пользователя из системы."""
    response = await authenticated_client.post("/users/logout/")
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь успешно вышел из системы"}

    # Проверяем, что защищенный эндпоинт недоступен после выхода
    response_after_logout = await authenticated_client.get("/users/me/")
    assert response_after_logout.status_code == 401 # Unauthorized