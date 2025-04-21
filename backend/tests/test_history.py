import pytest

@pytest.mark.asyncio
async def test_get_history(client):
    """Тест получения истории анализов."""
    response = await client.get("/history/all/")
    assert response.status_code in [200, 401]