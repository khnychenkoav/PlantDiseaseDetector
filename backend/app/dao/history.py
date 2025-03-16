import uuid
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repository.repository import async_session_maker
from app.dao.base import BaseDAO
from app.repository.models import History


class HistoryDAO(BaseDAO):
    model = History

    @classmethod
    async def create_record(
        cls, user_uuid: str, disease_uuid: str, image_path: str
    ) -> History:
        async with async_session_maker() as session:
            record = History(
                id=uuid.uuid4(),
                user_id=user_uuid,
                disease_id=disease_uuid,
                image_path=image_path,
            )
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record

    @classmethod
    async def get_history(cls, user_id: uuid.UUID):
        async with async_session_maker() as session:
            query = (
                select(History)
                .options(joinedload(History.user), joinedload(History.disease))
                .filter_by(user_id=user_id)
            )
            result = await session.execute(query)
            objects = result.scalars().all()
        return objects
