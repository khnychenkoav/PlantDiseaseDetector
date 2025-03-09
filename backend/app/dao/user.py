import uuid
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from typing import Dict, Any


from app.repository.repository import async_session_maker
from app.repository.models import User
from app.dao.base import BaseDAO
from app.services.security import get_password_hash


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def create_user(cls, name: str, email: str, password: str) -> User:
        async with async_session_maker() as session:
            hashed_password = get_password_hash(password)
            user = User(
                id=uuid.uuid4(), email=email, name=name, password=hashed_password
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @classmethod
    async def update_user(cls, update_data: Dict[str, Any]) -> User:
        async with async_session_maker() as session:
            result = await session.execute(
                select(User).where(User.email == update_data["email"])
            )
            user = result.scalars().first()

            if not user:
                raise NoResultFound(f"Пользователь не найден")

            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            await session.commit()
            await session.refresh(user)
            return user
