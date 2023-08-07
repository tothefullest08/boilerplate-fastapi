from pydantic import BaseModel


class ErrorContentResponse(BaseModel):
    type: str
    description: str


class ErrorResponse(BaseModel):
    status_code: int
    content: ErrorContentResponse
