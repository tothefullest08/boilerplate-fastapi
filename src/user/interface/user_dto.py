from datetime import datetime

from pydantic import BaseModel, Field


class JwtTokenDto(BaseModel):
    access_token: str = Field(..., description="액세스 토큰")
    refresh_token: str = Field(..., description="리프래시 토큰")


class UserTokenDto(BaseModel):
    id: int = Field(..., description="id")
    user_id: int = Field(..., description="유저 아이디")
    access_token: str = Field(..., description="액세스 토큰")
    refresh_token: str = Field(..., description="리프레시 토큰")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="업데이트 시간")
