import pytest
import uuid

from app.dao.history import HistoryDAO
from app.dao.user import UserDAO # Импортируем UserDAO
from app.repository.models import History as HistoryModel, User as UserModel, Disease as DiseaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
# sqlalchemy.orm.selectinload не используется напрямую в этих тестах, но полезно помнить о нем
# для проверки eager loading, если бы мы делали более сложные запросы здесь.

# Фикстуры test_user и test_disease должны быть доступны из conftest.py
# и они должны создавать записи в БД, чтобы мы могли использовать их ID.

@pytest.mark.asyncio
async def test_create_history_record(
    db_session: AsyncSession, # Используем сессию для прямых проверок
    test_user: UserModel,     # Фикстура пользователя из conftest
    test_disease: DiseaseModel # Фикстура болезни из conftest
):
    """Тестирует успешное создание записи в истории."""
    user_id = test_user.id
    disease_id = test_disease.id
    image_path = "/uploads/test_image_for_history.jpg"

    # Вызываем метод DAO для создания записи
    created_record = await HistoryDAO.create_record(
        user_uuid=user_id, 
        disease_uuid=disease_id,
        image_path=image_path
    )

    assert created_record is not None
    assert isinstance(created_record, HistoryModel)
    assert created_record.id is not None
    assert created_record.user_id == user_id
    assert created_record.disease_id == disease_id
    assert created_record.image_path == image_path
    assert created_record.created_at is not None # Проверяем, что дата создания установилась

    # Дополнительная проверка: получаем запись напрямую из БД
    # Коммит здесь не нужен, так как HistoryDAO.create_record уже делает коммит внутри своей сессии.
    # Если бы мы хотели проверить в той же сессии, что и DAO, нам бы не нужен был commit.
    # Но так как DAO использует свою сессию, а мы здесь используем db_session (другую инстанцию из пула),
    # то данные, закоммиченные DAO, должны быть видны.
    # await db_session.commit() # Этот коммит здесь не нужен и может быть вреден, если db_session имеет незавершенные транзакции.

    stmt = select(HistoryModel).where(HistoryModel.id == created_record.id)
    result = await db_session.execute(stmt) # db_session из фикстуры
    record_from_db = result.scalar_one_or_none()

    assert record_from_db is not None
    assert record_from_db.user_id == user_id
    assert record_from_db.disease_id == disease_id
    assert record_from_db.image_path == image_path

@pytest.mark.asyncio
async def test_get_history_for_user_with_records(
    db_session: AsyncSession, # db_session для создания "другого" пользователя
    test_user: UserModel,
    test_disease: DiseaseModel
):
    """Тестирует получение истории для пользователя с существующими записями."""
    user_id = test_user.id

    # Создаем несколько записей для этого пользователя
    record1 = await HistoryDAO.create_record(user_id, test_disease.id, "/path/img1.jpg")
    record2 = await HistoryDAO.create_record(user_id, test_disease.id, "/path/img2.jpg")
    
    # Создаем ДРУГОГО пользователя и запись для него
    other_user_email = f"other_user_{uuid.uuid4()}@example.com"
    other_user_name = "Other Test User"
    other_user_password = "otherpassword"
    
    # Используем UserDAO для создания другого пользователя
    # Предполагается, что UserDAO.create_user корректно создает и коммитит пользователя
    other_user = await UserDAO.create_user(
        name=other_user_name,
        email=other_user_email,
        password=other_user_password
    )
    # Если UserDAO.create_user не делает commit или refresh внутри, 
    # и мы хотим быть уверены, что он доступен для HistoryDAO,
    # можно было бы сделать db_session.commit() здесь, если UserDAO использует ту же сессию,
    # но DAO обычно инкапсулируют свои сессии.
    # HistoryDAO.create_record будет использовать свою сессию.
    
    await HistoryDAO.create_record(other_user.id, test_disease.id, "/path/img_other.jpg")


    # Получаем историю для test_user
    history_records = await HistoryDAO.get_history(user_id=user_id)

    assert history_records is not None
    assert isinstance(history_records, list)
    assert len(history_records) == 2 # Ожидаем 2 записи для test_user

    record_ids_from_db = {r.id for r in history_records}
    assert record1.id in record_ids_from_db
    assert record2.id in record_ids_from_db

    for record in history_records:
        assert isinstance(record, HistoryModel)
        assert record.user_id == user_id
        # Проверяем, что связанные объекты загружены (joinedload)
        assert record.user is not None 
        assert isinstance(record.user, UserModel)
        assert record.user.id == user_id
        
        assert record.disease is not None
        assert isinstance(record.disease, DiseaseModel)
        assert record.disease.id == test_disease.id # В данном тесте обе записи с одной болезнью

@pytest.mark.asyncio
async def test_get_history_for_user_with_no_records(
    test_user: UserModel # Пользователь, для которого мы не создавали историю
):
    """Тестирует получение истории для пользователя без записей."""
    # Фикстура test_user создает нового пользователя для каждого теста,
    # поэтому для этого конкретного экземпляра test_user еще не должно быть истории.
    
    history_records = await HistoryDAO.get_history(user_id=test_user.id)

    assert history_records is not None
    assert isinstance(history_records, list)
    assert len(history_records) == 0

@pytest.mark.asyncio
async def test_get_history_for_non_existent_user_id():
    """Тестирует получение истории для несуществующего user_id."""
    non_existent_user_id = uuid.uuid4() # Случайный UUID
    
    history_records = await HistoryDAO.get_history(user_id=non_existent_user_id)

    assert history_records is not None
    assert isinstance(history_records, list)
    assert len(history_records) == 0