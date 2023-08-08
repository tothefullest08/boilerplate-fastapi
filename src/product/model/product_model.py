from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from src.common.database.model import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(
        Integer().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    category = Column(String(32), comment="카테고리", nullable=False)
    price = Column(Integer, comment="가격", nullable=False)
    raw_price = Column(Integer, comment="원가", nullable=False)
    name = Column(String(64), comment="이름", index=True, nullable=False)
    description = Column(String(512), comment="설명", nullable=False)
    barcode = Column(String(128), comment="바코드", nullable=False)
    size = Column(String(32), comment="사이즈 (small or large)", nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
