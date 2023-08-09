from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.common.exception import InternalException
from src.common.exception.failure_type import FailureType
from src.product.controller import product_v1_router
from src.user.controller import user_v1_router


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(InternalException)
    async def custom_exception_handler(request: Request, e: InternalException):
        return JSONResponse(
            status_code=e.get_status_code(),
            content={
                "meta": {"code": e.get_status_code(), "message": e.get_error_type()},
                "data": None,
            },
        )

    @app_.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, e: RequestValidationError):
        return JSONResponse(
            status_code=FailureType.INPUT_PARAMETER_ERROR.status_code,
            content={
                "meta": {
                    "code": FailureType.INPUT_PARAMETER_ERROR.status_code,
                    "message": e.errors,
                },
                "data": None,
            },
        )


app = FastAPI(docs_url="/docs", openapi_url="/openapi.json")

app.include_router(user_v1_router, prefix="/api/v1")
app.include_router(product_v1_router, prefix="/api/v1")

init_listeners(app_=app)
