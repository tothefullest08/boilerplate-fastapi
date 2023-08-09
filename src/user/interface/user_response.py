from pydantic import BaseModel, Field

from src.common.response import BaseResponse
from src.user.interface.user_dto import UserTokenDto


class UserResponse(BaseModel):
    id: int = Field(..., description="id")
    name: str = Field(..., description="유저 이름")
    access_token: str = Field(..., description="액세스 토큰")


class UserTokenResponse(BaseResponse):
    data: UserTokenDto
