from datetime import datetime

from pydantic import BaseModel


class MetaResponse(BaseModel):
    code: int
    message: str


class BaseResponse(BaseModel):
    meta: MetaResponse

    class Config:
        json_encoders = {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}


class ErrorResponse(BaseResponse):
    data: None
