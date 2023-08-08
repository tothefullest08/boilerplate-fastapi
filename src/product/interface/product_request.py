from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.product.interface.product_enum import ProductSizeEnum


class ProductRequest(BaseModel):
    category: str = Field(..., description="카테고리")
    price: int = Field(..., description="가격")
    raw_price: str = Field(..., description="원가")
    name: str = Field(..., description="이름")
    description: str = Field(..., description="설명")
    barcode: str = Field(..., description="바코드")
    size: ProductSizeEnum = Field(..., description="사이즈")
    expiration_date: datetime = Field(..., description="유통기한")


class UpdateProductRequest(BaseModel):
    category: Optional[str] = Field(None, description="카테고리")
    price: Optional[int] = Field(None, description="가격")
    raw_price: Optional[str] = Field(None, description="원가")
    name: Optional[str] = Field(None, description="이름")
    description: Optional[str] = Field(None, description="설명")
    barcode: Optional[str] = Field(None, description="바코드")
    size: Optional[ProductSizeEnum] = Field(None, description="사이즈")
    expiration_date: Optional[datetime] = Field(None, description="유통기한")
