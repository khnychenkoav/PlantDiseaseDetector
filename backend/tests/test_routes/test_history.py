import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, MagicMock # Добавлены MagicMock и AsyncMock
from datetime import datetime, timedelta # Добавлены datetime и timedelta

# Предполагается, что фикстуры authenticated_client и test_user доступны из conftest.py
# и test_user имеет атрибут id

@pytest.mark.asyncio
async def test_get_history_unauthorized(client: AsyncClient):
    """Тестирует невозможность получения истории неаутентифицированным пользователем."""
    response = await client.get("/history/all/") # Убедитесь, что префикс роутера /history учтен, если он есть в main.py
    assert response.status_code == 401 # Unauthorized

@pytest.mark.asyncio
@patch("app.dao.history.HistoryDAO.get_history", new_callable=AsyncMock) # Мокаем DAO
async def test_get_history_authorized_no_history(
    mock_get_history: AsyncMock, 
    authenticated_client: AsyncClient,
    test_user: MagicMock # Используем test_user из conftest, который должен иметь id
):
    """
    Тестирует получение истории аутентифицированным пользователем,
    у которого еще нет записей в истории (ожидается пустой список).
    """
    mock_get_history.return_value = [] # DAO возвращает пустой список

    response = await authenticated_client.get("/history/all/")
    assert response.status_code == 200
    assert response.json() == [] # Ожидаем пустой список
    mock_get_history.assert_called_once_with(user_id=test_user.id)


@pytest.mark.asyncio
@patch("app.dao.history.HistoryDAO.get_history", new_callable=AsyncMock) # Мокаем DAO
async def test_get_history_authorized_with_history(
    mock_get_history: AsyncMock,
    authenticated_client: AsyncClient,
    test_user: MagicMock # Используем test_user из conftest
):
    """
    Тестирует получение истории аутентифицированным пользователем,
    у которого есть записи в истории.
    """
    # Создаем мок-объекты для имитации данных из БД
    mock_disease_1 = MagicMock()
    mock_disease_1.name = "Ржавчина яблони"
    mock_disease_1.reason = "Грибковое заболевание"
    mock_disease_1.recommendations = "Обработать фунгицидом"

    mock_record_1 = MagicMock()
    mock_record_1.disease = mock_disease_1
    mock_record_1.created_at = datetime.utcnow()
    mock_record_1.image_path = "/uploads/test_image1.jpg"
    
    mock_disease_2 = MagicMock()
    mock_disease_2.name = "Мучнистая роса"
    mock_disease_2.reason = "Еще одно грибковое заболевание"
    mock_disease_2.recommendations = "Обеспечить хорошую вентиляцию"

    mock_record_2 = MagicMock()
    mock_record_2.disease = mock_disease_2
    # Для корректной сериализации в JSON, datetime должен быть строкой или обработан FastAPI
    # В данном случае FastAPI (Pydantic) должен сам справиться с datetime объектом
    mock_record_2.created_at = datetime.utcnow() - timedelta(days=1) 
    mock_record_2.image_path = "/uploads/test_image2.jpg"

    mock_get_history.return_value = [mock_record_1, mock_record_2] # DAO возвращает список с данными

    response = await authenticated_client.get("/history/all/")

    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 2

    # Проверяем содержимое первого элемента
    # Убедимся, что время сериализовано в строку (обычно ISO формат)
    assert response_json[0]["diseases_name"] == "Ржавчина яблони"
    assert response_json[0]["reason"] == "Грибковое заболевание"
    assert response_json[0]["recommendation"] == "Обработать фунгицидом"
    assert response_json[0]["image_url"] == "/uploads/test_image1.jpg"
    assert "time" in response_json[0]
    # Проверка формата времени (опционально, но полезно)
    try:
        datetime.fromisoformat(response_json[0]["time"].replace("Z", "+00:00")) # Pydantic v2 может добавлять Z
    except ValueError:
        datetime.fromisoformat(response_json[0]["time"])


    # Проверяем содержимое второго элемента
    assert response_json[1]["diseases_name"] == "Мучнистая роса"
    assert response_json[1]["image_url"] == "/uploads/test_image2.jpg"
    assert "time" in response_json[1]

    mock_get_history.assert_called_once_with(user_id=test_user.id)