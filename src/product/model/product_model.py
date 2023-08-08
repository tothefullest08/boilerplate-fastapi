from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Index,
)

from src.common.database.model import Base


class ProductModel(Base):
    __tablename__ = "products"
    __table_args__ = (
        Index(
            "products_name_name_chosung_idx",
            "name",
            "name_chosung",
        ),
    )

    id = Column(
        Integer().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    user_id = Column(Integer, index=True, unique=True, nullable=False)
    category = Column(String(32), comment="카테고리", nullable=False)
    price = Column(Integer, comment="가격", nullable=False)
    raw_price = Column(Integer, comment="원가", nullable=False)
    name = Column(String(64), comment="이름", nullable=False)
    name_chosung = Column(String(64), comment="이름 초성", nullable=False)
    description = Column(String(512), comment="설명", nullable=False)
    barcode = Column(String(128), comment="바코드", nullable=False)
    size = Column(String(32), comment="사이즈 (small or large)", nullable=False)
    expiration_date = Column(DateTime, comment="유통기한", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
