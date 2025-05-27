import pytest
import io
import os
import uuid
import json
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
@patch("app.routes.disease.model_service.predict", new_callable=MagicMock)
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
@patch("app.routes.disease.model_service.predict", new_callable=MagicMock)
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

# --- Тесты для эндпоинта /diseases/create/init/ ---

@pytest.mark.asyncio
@patch("app.routes.disease.open", new_callable=mock_open)
async def test_init_diseases_file_not_found(
    mock_file_open: MagicMock,
    authenticated_admin_client: AsyncClient
):
    """
    Тестирует эндпоинт /diseases/create/init/, когда файл class_disease.json не найден.
    """
    mock_file_open.side_effect = FileNotFoundError("File not found for testing")
    response = await authenticated_admin_client.post("/diseases/create/init/")
    assert response.status_code == 500
    assert "Ошибка чтения файла" in response.json()["detail"]
    assert "File not found for testing" in response.json()["detail"]


@pytest.mark.asyncio
@patch("app.routes.disease.open", new_callable=mock_open)
@patch("app.dao.disease.DiseaseDAO.find_one_or_none", new_callable=AsyncMock)
@patch("app.dao.disease.DiseaseDAO.create_record", new_callable=AsyncMock)
async def test_init_diseases_success_with_duplicates_and_new(
    mock_dao_create: AsyncMock,
    mock_dao_find: AsyncMock,
    mock_file_open: MagicMock,
    authenticated_admin_client: AsyncClient,
    test_disease: DiseaseModel # Фикстура для имитации существующей болезни
):
    """
    Тестирует /diseases/create/init/ с успешным созданием новых
    и обнаружением существующих болезней.
    """
    diseases_data = [
        {"ru": "Новая Болезнь 1", "cause": "Причина 1", "treatment": "Лечение 1"},
        {"ru": test_disease.name, "cause": "Уже есть", "treatment": "Обновить?"}, # Существующая
        {"ru": "Новая Болезнь 2", "cause": "Причина 2", "treatment": "Лечение 2"},
    ]
    mock_file_open.return_value.read.return_value = json.dumps(diseases_data) # Импортируйте json

    # Настройка mock_dao_find:
    # 1. Новая Болезнь 1 -> None (не найдена)
    # 2. test_disease.name -> test_disease (найдена)
    # 3. Новая Болезнь 2 -> None (не найдена)
    def find_side_effect(name):
        if name == test_disease.name:
            return test_disease
        return None
    mock_dao_find.side_effect = find_side_effect
    mock_dao_create.return_value = None # Успешное создание

    response = await authenticated_admin_client.post("/diseases/create/init/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["created"] == 2 # "Новая Болезнь 1" и "Новая Болезнь 2"
    assert data["duplicates"] == 1 # test_disease.name
    assert data["total_processed"] == 3

    assert mock_dao_find.call_count == 3
    assert mock_dao_create.call_count == 2
    mock_dao_create.assert_any_call("Новая Болезнь 1", "Причина 1", "Лечение 1")
    mock_dao_create.assert_any_call("Новая Болезнь 2", "Причина 2", "Лечение 2")


@pytest.mark.asyncio
@patch("app.routes.disease.open", new_callable=mock_open)
@patch("app.dao.disease.DiseaseDAO.find_one_or_none", new_callable=AsyncMock)
@patch("app.dao.disease.DiseaseDAO.create_record", new_callable=AsyncMock)
async def test_init_diseases_creation_error_continues(
    mock_dao_create: AsyncMock,
    mock_dao_find: AsyncMock,
    mock_file_open: MagicMock,
    authenticated_admin_client: AsyncClient
):
    """
    Тестирует /diseases/create/init/, когда DiseaseDAO.create_record вызывает ошибку
    для одной из записей, но процесс продолжается для других.
    """
    diseases_data = [
        {"ru": "Болезнь А", "cause": "Причина А", "treatment": "Лечение А"},
        {"ru": "Болезнь Б (ошибка)", "cause": "Причина Б", "treatment": "Лечение Б"},
        {"ru": "Болезнь В", "cause": "Причина В", "treatment": "Лечение В"},
    ]
    mock_file_open.return_value.read.return_value = json.dumps(diseases_data)
    mock_dao_find.return_value = None # Все болезни считаются новыми

    # Настройка mock_dao_create:
    # 1. Болезнь А -> успешно
    # 2. Болезнь Б (ошибка) -> вызывает Exception
    # 3. Болезнь В -> успешно
    def create_side_effect(name, reason, recommendation):
        if name == "Болезнь Б (ошибка)":
            raise Exception("DB error on create")
        return None # Успешное создание для других
    mock_dao_create.side_effect = create_side_effect

    response = await authenticated_admin_client.post("/diseases/create/init/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["created"] == 2 # "Болезнь А" и "Болезнь В"
    assert data["duplicates"] == 0
    assert data["total_processed"] == 3

    assert mock_dao_create.call_count == 3 # Было 3 попытки создания


# --- Тесты для эндпоинта /diseases/all/ ---

@pytest.mark.asyncio
@patch("app.dao.disease.DiseaseDAO.find_all", new_callable=AsyncMock)
async def test_get_all_diseases_empty_db(
    mock_find_all: AsyncMock,
    authenticated_client: AsyncClient # Можно использовать обычного пользователя, если доступ разрешен
):
    """
    Тестирует эндпоинт /diseases/all/, когда в базе данных нет болезней.
    """
    mock_find_all.return_value = [] # DAO возвращает пустой список
    response = await authenticated_client.get("/diseases/all/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
@patch("app.dao.disease.DiseaseDAO.find_all", new_callable=AsyncMock)
async def test_get_all_diseases_with_data(
    mock_find_all: AsyncMock,
    authenticated_client: AsyncClient, # или authenticated_admin_client, если требуется админ
    test_disease: DiseaseModel # Используем фикстуру для тестовых данных
):
    """
    Тестирует эндпоинт /diseases/all/, когда в базе данных есть болезни.
    """
    # Создаем мок-объект, похожий на то, что возвращает DAO
    # DiseaseDAO.find_all() обычно возвращает список объектов DiseaseModel
    mock_disease_1 = DiseaseModel(
        id=uuid.uuid4(),
        name="Тестовая Болезнь 1 из all",
        reason="Причина 1",
        recommendations="Рекомендация 1"
    )
    mock_disease_2 = test_disease # Используем существующую фикстуру
    mock_find_all.return_value = [mock_disease_1, mock_disease_2]

    response = await authenticated_client.get("/diseases/all/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Проверяем, что данные в ответе соответствуют мок-объектам
    # Порядок может быть не гарантирован, поэтому лучше проверять наличие
    expected_names = {mock_disease_1.name, mock_disease_2.name}
    response_names = {item["name"] for item in data}
    assert response_names == expected_names

    for item in data:
        if item["name"] == mock_disease_1.name:
            assert item["reason"] == mock_disease_1.reason
            assert item["recommendation"] == mock_disease_1.recommendations
        elif item["name"] == mock_disease_2.name:
            assert item["reason"] == mock_disease_2.reason
            assert item["recommendation"] == mock_disease_2.recommendations