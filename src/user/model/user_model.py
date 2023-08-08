from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from src.common.database.model import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        Integer().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    phone_number = Column(
        String(32), comment="핸드폰 번호", index=True, unique=True, nullable=False
    )
    password = Column(String(256), comment="비밀 번호", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class UserTokenModel(Base):
    __tablename__ = "user_tokens"

    id = Column(
        Integer().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    user_id = Column(Integer, index=True, unique=True, nullable=False)
    access_token = Column(String(256), comment="액세스 토큰", nullable=False)
    refresh_token = Column(String(256), comment="리프레시 토큰", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
