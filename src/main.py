from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.common.exception import InternalException
from src.common.exception.failure_type import FailureType
from src.user.controller import user_router


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(InternalException)
    async def custom_exception_handler(request: Request, e: InternalException):
        return JSONResponse(
            status_code=e.get_status_code(),
            content={"type": e.get_error_type(), "description": e.get_description()},
        )

    @app_.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, e: RequestValidationError):
        return JSONResponse(
            status_code=FailureType.INPUT_PARAMETER_ERROR.status_code,
            content={
                "type": FailureType.INPUT_PARAMETER_ERROR.error_type,
                "description": e.errors(),
            },
        )


app = FastAPI(docs_url="/docs", openapi_url="/openapi.json")
app.include_router(user_router)
init_listeners(app_=app)
