import uuid


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
