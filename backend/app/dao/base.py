from sqlalchemy.future import select
from app.repository.repository import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Находит все записи в базе данных по переданным фильтрам.
        Возвращает список объектов.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            objects = result.scalars().all()
            return objects

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Находит одну запись в базе данных по переданным фильтрам.
        Возвращает объект модели или None, если запись не найдена.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().first()
