import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_history_unauthorized(client: AsyncClient):
    """Тестирует невозможность получения истории неаутентифицированным пользователем."""
    response = await client.get("/history/all/")
    assert response.status_code == 401 # Unauthorized

@pytest.mark.asyncio
async def test_get_history_authorized_no_history(authenticated_client: AsyncClient):
    """
    Тестирует получение истории аутентифицированным пользователем,
    у которого еще нет записей в истории (ожидается пустой список).
    """
    response = await authenticated_client.get("/history/all/")
    assert response.status_code == 200
    assert response.json() == [] # Ожидаем пустой список