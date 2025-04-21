import os
import sys
import asyncio
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Добавление пути для импортов (если в тестах нужно что-то из вашего проекта)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from main import app

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://testserver", transport=ASGITransport(app=app)) as c:
        yield c