import uuid

from app.repository.repository import async_session_maker
from app.dao.base import BaseDAO
from app.repository.models import Disease


class DiseaseDAO(BaseDAO):
    model = Disease

    @classmethod
    async def create_record(
        cls,
        name: str,
        reason: str,
        recommendation: str,
    ) -> Disease:
        async with async_session_maker() as session:
            record = Disease(
                id=uuid.uuid4(),
                name=name,
                reason=reason,
                recommendations=recommendation,
            )
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record
