from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from src.common.config import config

engines = {
    "cluster": create_engine(config.WRITER_DB_URL, poolclass=NullPool),
}

SessionLocal = sessionmaker(bind=engines["cluster"], autocommit=False, autoflush=False)
Base = declarative_base()
