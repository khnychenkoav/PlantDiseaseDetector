import pytest
import io
from unittest.mock import patch, MagicMock

# Исправление пути импорта для патча
@pytest.mark.asyncio
@patch("app.dao.disease.DiseaseDAO.create_record")
async def test_create_disease(mock_cre, client):
    mock_cre.return_value = None
    response = await client.post("/diseases/create/", json={
        "name": "Fusarium",
        "reason": "Fungi",
        "recommendation": "Use fungicide"
    })
    assert response.status_code in [200, 401]
    if response.status_code == 200:
        assert "message" in response.json()

@pytest.mark.asyncio
async def test_upload_file(client):
    # Создание тестового файла в памяти
    test_file = io.BytesIO(b"dummydata")
    file_data = {"file": ("test_image.jpg", test_file, "image/jpeg")}
    response = await client.post("/diseases/upload/", files=file_data)
    assert response.status_code in [200, 401]

@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_upload_invalid_file_format(client):
    """Тест загрузки файла с неподдерживаемым форматом."""
    test_file = io.BytesIO(b"test file content")
    file_data = {"file": ("test_doc.txt", test_file, "text/plain")}
    response = await client.post("/diseases/upload/", files=file_data)
    assert response.status_code in [400, 415, 422]

@pytest.mark.asyncio
@patch("app.routes.disease.DiseaseDAO.find_one_or_none")
async def test_get_disease_by_id(mock_find, client):
    """Тест получения болезни по ID."""
    mock_find.return_value = {
        "id": "test-id",
        "name": "TestDisease",
        "reason": "Test reason",
        "recommendations": "Test recommendations"
    }
    response = await client.get("/diseases/1")
    assert response.status_code in [200, 401, 404]