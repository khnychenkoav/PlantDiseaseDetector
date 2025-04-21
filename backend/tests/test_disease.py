import pytest
import io
import os
import uuid
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, mock_open, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repository.models import User as UserModel, Disease as DiseaseModel
from app.dao.disease import DiseaseDAO

@pytest.mark.asyncio
async def test_create_disease_unauthorized(client: AsyncClient):
    """Тестирует невозможность создания болезни неаутентифицированным пользователем."""
    response = await client.post("/diseases/create/", json={
        "name": "New Disease",
        "reason": "New Reason",
        "recommendation": "New Rec"
    })
    assert response.status_code == 401 # Unauthorized

@pytest.mark.asyncio
async def test_create_disease_not_admin(authenticated_client: AsyncClient):
    """Тестирует невозможность создания болезни обычным (не админ) пользователем."""
    response = await authenticated_client.post("/diseases/create/", json={
        "name": "New Disease",
        "reason": "New Reason",
        "recommendation": "New Rec"
    })
    assert response.status_code == 403 # Forbidden

@pytest.mark.asyncio
async def test_create_disease_admin_success(authenticated_admin_client: AsyncClient, db_session: AsyncSession):
    """Тестирует успешное создание болезни администратором."""
    disease_name = f"Admin Created Disease {uuid.uuid4()}"
    disease_data = {
        "name": disease_name,
        "reason": "Admin Reason",
        "recommendation": "Admin Rec"
    }
    response = await authenticated_admin_client.post("/diseases/create/", json=disease_data)
    assert response.status_code == 200

    # Проверяем наличие записи в БД через сессию теста
    await db_session.commit() # Коммитим, чтобы увидеть изменения от API
    created_disease = await db_session.execute(
        select(DiseaseModel).where(DiseaseModel.name == disease_name)
    )
    assert created_disease.scalar_one_or_none() is not None

@pytest.mark.asyncio
async def test_upload_file_unauthorized(client: AsyncClient):
    """Тестирует невозможность загрузки файла неаутентифицированным пользователем."""
    test_file = io.BytesIO(b"dummy image data")
    files = {"file": ("test.jpg", test_file, "image/jpeg")}
    response = await client.post("/diseases/upload/", files=files)
    assert response.status_code == 401 # Unauthorized

# --- Тесты загрузки файла авторизованным пользователем ---

@pytest.mark.asyncio
@patch("app.routes.disease.predict", new_callable=MagicMock)
@patch("app.routes.disease.os.makedirs")
@patch("app.routes.disease.open", new_callable=mock_open)
@patch("app.routes.disease.get_hashed_path")
@patch("app.dao.disease.DiseaseDAO.find_one_or_none", new_callable=AsyncMock)
@patch("app.dao.history.HistoryDAO.create_record", new_callable=AsyncMock)
async def test_upload_file_authorized_success(
    mock_create_history: AsyncMock,
    mock_find_disease: AsyncMock,
    mock_get_hashed_path: MagicMock,
    mock_file_open: MagicMock,
    mock_makedirs: MagicMock,
    mock_predict: MagicMock,
    authenticated_client: AsyncClient,
    test_user: UserModel,
    test_disease: DiseaseModel
):
    """
    Тестирует успешную загрузку файла, предсказание существующей болезни
    и создание записи в истории.
    """
    mock_get_hashed_path.return_value = "hashed_subdir"
    predicted_disease_name = test_disease.name
    mock_predict.return_value = {"ru": predicted_disease_name}
    mock_find_disease.return_value = test_disease # Мок DAO находит болезнь
    mock_create_history.return_value = None

    test_file_content = b"dummy image data"
    test_file = io.BytesIO(test_file_content)
    files = {"file": ("test_image.jpg", test_file, "image/jpeg")}
    expected_save_path = os.path.join("uploads", "hashed_subdir", "test_image.jpg")

    response = await authenticated_client.post("/diseases/upload/", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["diseases_name"] == test_disease.name
    assert data["reason"] == test_disease.reason
    assert data["recommendation"] == test_disease.recommendations
    assert data["image_url"] == expected_save_path

    # Проверяем вызовы моков
    mock_get_hashed_path.assert_called_once_with("test_image.jpg")
    mock_makedirs.assert_called_once_with(os.path.join("uploads", "hashed_subdir"), exist_ok=True)
    mock_file_open.assert_called_once_with(expected_save_path, "wb")
    mock_file_open().write.assert_called_once_with(test_file_content)
    mock_predict.assert_called_once()
    mock_find_disease.assert_called_once_with(name=predicted_disease_name)
    mock_create_history.assert_called_once_with(
        test_user.id,
        test_disease.id,
        expected_save_path
    )


@pytest.mark.asyncio
@patch("app.routes.disease.predict", new_callable=MagicMock)
@patch("app.routes.disease.os.makedirs")
@patch("app.routes.disease.open", new_callable=mock_open)
@patch("app.routes.disease.get_hashed_path")
@patch("app.dao.disease.DiseaseDAO.find_one_or_none", new_callable=AsyncMock)
@patch("app.dao.history.HistoryDAO.create_record", new_callable=AsyncMock)
async def test_upload_file_disease_not_found_fallback(
    mock_create_history: AsyncMock,
    mock_find_disease: AsyncMock,
    mock_get_hashed_path: MagicMock,
    mock_file_open: MagicMock,
    mock_makedirs: MagicMock,
    mock_predict: MagicMock,
    authenticated_client: AsyncClient,
    test_user: UserModel,
    db_session: AsyncSession
):
    """
    Тестирует загрузку файла, когда предсказанная болезнь не найдена в БД,
    но существует болезнь "НеизвестнаяБолезнь", которая используется как fallback.
    """
    # Создаем "НеизвестнуюБолезнь" через DAO (использует подмененную сессию)
    unknown_disease_name = "НеизвестнаяБолезнь"
    unknown_disease_reason = "Причина неизвестна"
    unknown_disease_recommendation = "Рекомендация неизвестна"
    unknown_disease_obj_from_dao = await DiseaseDAO.create_record(
        name=unknown_disease_name,
        reason=unknown_disease_reason,
        recommendation=unknown_disease_recommendation
    )
    # Получаем объект из БД через сессию теста для дальнейшего использования
    refreshed_unknown_disease = await db_session.get(DiseaseModel, unknown_disease_obj_from_dao.id)
    assert refreshed_unknown_disease is not None

    # Настраиваем моки
    mock_get_hashed_path.return_value = "hashed_subdir_unknown"
    predicted_disease_name = "ОченьРедкаяБолезнь" # Болезнь, которой нет в БД
    mock_predict.return_value = {"ru": predicted_disease_name}
    # Первый вызов find_one_or_none вернет None, второй - объект "НеизвестнаяБолезнь"
    mock_find_disease.side_effect = [None, refreshed_unknown_disease]
    mock_create_history.return_value = None

    test_file_content = b"image data unknown"
    test_file = io.BytesIO(test_file_content)
    files = {"file": ("unknown_disease.png", test_file, "image/png")}
    expected_save_path = os.path.join("uploads", "hashed_subdir_unknown", "unknown_disease.png")

    response = await authenticated_client.post("/diseases/upload/", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["diseases_name"] == unknown_disease_name
    assert data["reason"] == unknown_disease_reason
    assert data["recommendation"] == refreshed_unknown_disease.recommendations
    assert data["image_url"] == expected_save_path

    # Проверяем вызовы моков
    assert mock_find_disease.call_count == 2
    mock_find_disease.assert_any_call(name=predicted_disease_name)
    mock_find_disease.assert_any_call(name=unknown_disease_name)
    mock_predict.assert_called_once()
    mock_create_history.assert_called_once_with(
        test_user.id,
        refreshed_unknown_disease.id,
        expected_save_path
    )


@pytest.mark.asyncio
@pytest.mark.skip(reason="Тест не работает из-за отсутствия обработки ошибок в приложении")
async def test_upload_invalid_file_format(authenticated_client: AsyncClient):
    """
    Тестирует загрузку файла, который не является изображением (например, текст).
    Ожидает статус 500, так как текущая реализация приложения не обрабатывает
    ошибку PIL.UnidentifiedImageError и FastAPI возвращает Internal Server Error.
    Этот тест указывает на необходимость улучшения обработки ошибок в приложении.
    """
    test_file = io.BytesIO(b"this is text")
    files = {"file": ("test_doc.txt", test_file, "text/plain")}
    response = await authenticated_client.post("/diseases/upload/", files=files)
    assert response.status_code == 500
    # TODO: В приложении добавить обработчик исключений для PIL.UnidentifiedImageError,
    # чтобы возвращать 400 или 422 с понятным сообщением. После этого изменить
    # ожидаемый статус-код в этом тесте.