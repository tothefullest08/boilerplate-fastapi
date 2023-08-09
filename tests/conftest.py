import os
import random
import string
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
    try:
        Base.metadata.create_all(_db_conn)
        app.dependency_overrides[get_db] = get_test_db
        yield
    finally:
        drop_database(url)


def get_test_db() -> AsyncIterable[Session]:
    sess = Session(bind=_db_conn)
    try:
        yield sess
    finally:
        sess.close()


@pytest.fixture(scope="session")
def test_session():
    connection = _db_conn.connect()
    db = sessionmaker(bind=connection)
    session = db()
    yield session

    for tbl in reversed(Base.metadata.sorted_tables):
        session.rollback()
        connection.execute(tbl.delete())
    session.close()


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def generate_random_phone_numer():
    first = "010"
    second = "".join(random.choice(string.digits) for _ in range(4))
    third = "".join(random.choice(string.digits) for _ in range(4))
    return "{}-{}-{}".format(first, second, third)
