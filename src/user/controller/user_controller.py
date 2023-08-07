from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Header

from src.common.auth import AuthValidator
from src.common.database import get_db
from src.common.exception import FailureType
from src.common.response import ErrorResponse
from src.user.interface.user_response import UserResponse, GetUsersResponse
from src.user.service.user_service import UserService

router = APIRouter()


@router.get(
    path="/",
    response_model=GetUsersResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": f"{FailureType.GET_DATA_ERROR.error_type}",
        },
    },
    description="사용자 목록 조회",
)
def get_users(
    user_token: str = Header(None),
    session: Session = Depends(get_db),
):
    AuthValidator.validate_user_token(user_token)
    users = UserService(session=session).get_users()

    return GetUsersResponse(
        count=len(users),
        payload=[
            UserResponse(
                id=user.id,
                name=user.name,
                access_token=user.access_token,
            )
            for user in users
        ],
    )
