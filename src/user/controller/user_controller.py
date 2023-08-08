from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.common.database import get_db
from src.common.exception import FailureType
from src.common.response import ErrorResponse
from src.user.interface.user_dto import UserTokenDto
from src.user.interface.user_request import UserRequest
from src.user.interface.user_response import UserTokenResponse
from src.user.service.user_service import UserService

router = APIRouter()


@router.post(
    path="/sign-in",
    response_model=UserTokenResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": f"{FailureType.NOT_AUTHORIZED_ERROR.error_type}",
        },
        400: {
            "model": ErrorResponse,
            "description": f"{FailureType.UPSERT_DATA_ERROR.error_type}",
        },
    },
    description="로그인",
)
def sign_up(request: UserRequest, session: Session = Depends(get_db)):
    user_token = UserService(session_=session).sign_in(
        phone_number=request.phone_number, password=request.password
    )

    return {
        "meta": {"code": 200, "message": "ok"},
        "data": user_token,
    }


@router.post(
    path="/sign-up",
    response_model=UserTokenResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": f"{FailureType.NOT_AUTHORIZED_ERROR.error_type}",
        },
        400: {
            "model": ErrorResponse,
            "description": f"{FailureType.INPUT_PARAMETER_ERROR.error_type}"
            f"\n\n{FailureType.CREATE_DATA_ERROR.error_type}"
            f"\n\n{FailureType.UPSERT_DATA_ERROR.error_type}",
        },
    },
    description="회원 가입",
)
def sign_up(request: UserRequest, session: Session = Depends(get_db)):
    user_token = UserService(session_=session).sign_up(
        phone_number=request.phone_number, password=request.password
    )

    return {
        "meta": {"code": 200, "message": "ok"},
        "data": user_token,
    }
