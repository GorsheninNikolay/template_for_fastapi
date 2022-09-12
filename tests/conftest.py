# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from asyncio import new_event_loop, set_event_loop
from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.__main__ import get_app
from app.config import get_settings
from app.db.connection import SessionManager
from tests.utils import make_alembic_config


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    loop = new_event_loop()
    set_event_loop(loop)

    yield loop
    loop.close()


@pytest.fixture
async def postgres() -> str:
    """
    Создает временную БД для запуска теста.
    """
    settings = get_settings()

    tmp_name = ".".join([uuid4().hex, "pytest"])
    settings.DATABASE_NAME = tmp_name
    environ["POSTGRES_DB"] = tmp_name

    tmp_url = settings.database_uri_sync
    if not database_exists(tmp_url):
        create_database(tmp_url)
    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture
async def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(
        config="app/db/migrator/",
        name="alembic",
        pg_url=postgres,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)


@pytest.fixture
async def migrated_postgres(alembic_config: Config):
    """
    Проводит миграции.
    """
    upgrade(alembic_config, "head")


@pytest.fixture
async def client(
    migrated_postgres, manager: SessionManager = SessionManager()
) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    manager.refresh()
    yield AsyncClient(app=app, base_url="http://test")


@pytest.fixture
async def database(
    postgres, migrated_postgres, manager: SessionManager = SessionManager()
) -> Session:
    """
    Returns a class object with which you can create a new session to connect to the database.
    """
    manager.refresh()
    session_maker = manager.get_session_maker()
    async with session_maker() as database:
        try:
            yield database
        finally:
            await database.close()
