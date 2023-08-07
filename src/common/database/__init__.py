from typing import Any, Generator

from src.common.database.session import SessionLocal


# noinspection PyUnboundLocalVariable
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
