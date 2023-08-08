import os
from typing import AsyncIterable, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

os.environ["ENV"] = "testing"

from src.common.config import config as app_config
from src.common.database import get_db
from src.common.database.model import Base
from src.main import app

url = app_config.WRITER_DB_URL
_db_conn = create_engine(url)


def get_test_db() -> AsyncIterable[Session]:
    sess = Session(bind=_db_conn)
    try:
        yield sess
    finally:
        sess.close()


@pytest.fixture(scope="session")
def inject_session():
    def _inject_session(url: str):
        db_conn = create_engine(url)
        session = Session(bind=db_conn)
        return session

    return _inject_session


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    if database_exists(url):
        drop_database(url)
    create_database(url)
    Base.metadata.create_all(_db_conn)
    app.dependency_overrides[get_db] = get_test_db
    yield
    drop_database(url)


@pytest.fixture
def test_session():
    connection = _db_conn.connect()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session

    for tbl in reversed(Base.metadata.sorted_tables):
        session.rollback()
        connection.execute(tbl.delete())
    session.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
