from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.product.interface.product_enum import ProductSizeEnum


class ProductDto(BaseModel):
    id: int = Field(..., description="id")
    user_id: int = Field(..., description="유저 아이디")
    category: str = Field(..., description="카테고리")
    price: int = Field(..., description="가격")
    raw_price: str = Field(..., description="원가")
    name: str = Field(..., description="이름")
    description: str = Field(..., description="설명")
    barcode: str = Field(..., description="바코드")
    size: ProductSizeEnum = Field(..., description="사이즈")
    expiration_date: datetime = Field(..., description="유통기한")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="업데이트 시간")
