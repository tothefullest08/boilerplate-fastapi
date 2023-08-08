from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    phone_number: str = Field(..., description="전화번호")
    password: str = Field(..., description="비밀번호")
