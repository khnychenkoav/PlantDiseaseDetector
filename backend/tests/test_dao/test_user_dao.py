import pytest
import uuid
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.dao.user import UserDAO
from app.repository.models import User as UserModel
from app.services.security import get_password_hash, verify_password # verify_password для проверки хеша

# Фикстура test_user из conftest.py может быть полезна для некоторых тестов,
# но для тестирования create_user мы будем создавать пользователей напрямую.

@pytest.mark.asyncio
async def test_create_user_success(db_session: AsyncSession):
    """Тестирует успешное создание пользователя."""
    user_name = "Test User One"
    user_email = f"test_user_one_{uuid.uuid4()}@example.com"
    user_password = "testpassword123"

    created_user = await UserDAO.create_user(
        name=user_name, email=user_email, password=user_password
    )

    assert created_user is not None
    assert isinstance(created_user, UserModel)
    assert created_user.id is not None
    assert created_user.email == user_email
    assert created_user.name == user_name
    assert created_user.password != user_password # Пароль должен быть хеширован
    assert verify_password(user_password, created_user.password) # Проверяем хеш

    # Проверка в БД
    stmt = select(UserModel).where(UserModel.id == created_user.id)
    result = await db_session.execute(stmt)
    user_from_db = result.scalar_one_or_none()

    assert user_from_db is not None
    assert user_from_db.email == user_email
    assert verify_password(user_password, user_from_db.password)

@pytest.mark.asyncio
async def test_update_user_success(db_session: AsyncSession):
    """Тестирует успешное обновление данных пользователя."""
    # 1. Создаем пользователя
    original_name = "Original Name"
    original_email = f"original_{uuid.uuid4()}@example.com"
    original_password = "original_password"
    
    user_to_update = await UserDAO.create_user(
        name=original_name, email=original_email, password=original_password
    )
    assert user_to_update is not None

    # 2. Готовим данные для обновления
    updated_name = "Updated Name"
    updated_password_plain = "updated_password123"
    
    update_data: Dict[str, Any] = {
        "email": original_email, # Ключ для поиска пользователя
        "name": updated_name,
        "password": get_password_hash(updated_password_plain) # Обновляем хешированный пароль
    }

    # 3. Обновляем пользователя
    updated_user = await UserDAO.update_user(update_data)

    assert updated_user is not None
    assert updated_user.id == user_to_update.id
    assert updated_user.email == original_email # Email не должен меняться этим методом, если он ключ поиска
    assert updated_user.name == updated_name
    assert verify_password(updated_password_plain, updated_user.password)
    assert not verify_password(original_password, updated_user.password) # Убедимся, что старый пароль не подходит

    # 4. Проверка в БД
    stmt = select(UserModel).where(UserModel.id == updated_user.id)
    result = await db_session.execute(stmt)
    user_from_db = result.scalar_one_or_none()

    assert user_from_db is not None
    assert user_from_db.name == updated_name
    assert verify_password(updated_password_plain, user_from_db.password)

@pytest.mark.asyncio
async def test_update_user_not_found():
    """Тестирует обновление пользователя, который не найден (должно выбросить NoResultFound)."""
    non_existent_email = f"notfound_{uuid.uuid4()}@example.com"
    update_data: Dict[str, Any] = {
        "email": non_existent_email,
        "name": "Any Name"
    }

    with pytest.raises(NoResultFound) as exc_info:
        await UserDAO.update_user(update_data)
    
    assert f"Пользователь не найден" in str(exc_info.value)

@pytest.mark.asyncio
async def test_update_user_no_valid_fields_to_update(db_session: AsyncSession):
    """Тестирует обновление пользователя, когда в update_data нет валидных полей для модели User."""
    # 1. Создаем пользователя
    user_name = "Unchanged User"
    user_email = f"unchanged_{uuid.uuid4()}@example.com"
    user_password = "unchanged_password"
    
    user_instance = await UserDAO.create_user(
        name=user_name, email=user_email, password=user_password
    )
    assert user_instance is not None

    # 2. Готовим данные с невалидными полями
    update_data: Dict[str, Any] = {
        "email": user_email, # Ключ для поиска
        "non_existent_field": "some_value",
        "another_bad_key": 123
    }

    # 3. Обновляем пользователя
    updated_user = await UserDAO.update_user(update_data)

    assert updated_user is not None
    assert updated_user.id == user_instance.id
    assert updated_user.name == user_name # Имя не должно измениться
    assert updated_user.email == user_email # Email не должен измениться
    assert verify_password(user_password, updated_user.password) # Пароль не должен измениться

    # 4. Проверка в БД (на всякий случай)
    stmt = select(UserModel).where(UserModel.id == updated_user.id)
    result = await db_session.execute(stmt)
    user_from_db = result.scalar_one_or_none()
    assert user_from_db is not None
    assert user_from_db.name == user_name

@pytest.mark.asyncio
async def test_update_user_empty_update_data(db_session: AsyncSession):
    """Тестирует обновление пользователя с пустым словарем update_data (кроме email для поиска)."""
    # 1. Создаем пользователя
    user_name = "Empty Update User"
    user_email = f"empty_update_{uuid.uuid4()}@example.com"
    user_password = "empty_update_password"
    
    user_instance = await UserDAO.create_user(
        name=user_name, email=user_email, password=user_password
    )
    assert user_instance is not None

    # 2. Готовим пустые данные для обновления (только email для поиска)
    update_data: Dict[str, Any] = {
        "email": user_email 
    }

    # 3. Обновляем пользователя
    updated_user = await UserDAO.update_user(update_data)

    assert updated_user is not None
    assert updated_user.id == user_instance.id
    assert updated_user.name == user_name # Имя не должно измениться
    assert updated_user.email == user_email # Email не должен измениться
    assert verify_password(user_password, updated_user.password) # Пароль не должен измениться

    # 4. Проверка в БД
    stmt = select(UserModel).where(UserModel.id == updated_user.id)
    result = await db_session.execute(stmt)
    user_from_db = result.scalar_one_or_none()
    assert user_from_db is not None
    assert user_from_db.name == user_name