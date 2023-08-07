from typing import List

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int = Field(..., description="id")
    name: str = Field(..., description="유저 이름")
    access_token: str = Field(..., description="액세스 토큰")


class GetUsersResponse(BaseModel):
    count: int
    payload: List[UserResponse]
