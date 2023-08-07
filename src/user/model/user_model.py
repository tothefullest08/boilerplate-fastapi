from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String, DateTime,
)

from src.common.database.session import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(
        Integer().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    phone_number = Column(String(32), comment="핸드폰 번호")
    password = Column(String(256), comment="비밀 번호")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class UserTokenModel(Base):
    __tablename__ = "user_token"

    id = Column(
        Integer().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    access_token = Column(String(256), comment="액세스 토큰")
    refresh_token = Column(String(256), comment="리프레시 토큰")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
