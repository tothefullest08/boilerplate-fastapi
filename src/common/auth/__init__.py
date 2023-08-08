from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.common.config import config
from src.common.database import get_db
from src.common.exception import InternalException, FailureType
from src.common.logger import Logger
from src.user.repository.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/users/sign-in", scheme_name="JWT", auto_error=False
)


class JwtTokenizer:
    @staticmethod
    def encode(
        payload: dict,
        token_expire_minutes: int = 1440,
        key: str = config.ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> str:
        token = jwt.encode(
            claims={
                **payload,
                "exp": datetime.utcnow() + timedelta(minutes=token_expire_minutes),
            },
            key=key,
            algorithm=config.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode(
        token: str,
        key: str = config.ACCESS_TOKEN_SECRET,
    ) -> dict:
        return jwt.decode(
            token,
            key=key,
            algorithms=config.JWT_ALGORITHM,
        )


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)
) -> int:
    try:
        payload = JwtTokenizer.decode(token, key=config.ACCESS_TOKEN_SECRET)
        user_id: int = payload.get("user_id")
        if user_id is None:
            Logger().error(f" 헤더 토큰에 유저 아이디 없음. token: {token}")
            raise InternalException(FailureType.UNAUTHORIZED_TOKEN_ERROR, "")
    except JWTError:
        Logger().error(f" 토큰 시그니처가 유효하지 않음. token: {token}")
        raise InternalException(FailureType.UNAUTHORIZED_TOKEN_ERROR)
    except Exception:
        Logger().error(f" 그외 토큰 에러. token: {token}")
        raise InternalException(FailureType.UNAUTHORIZED_TOKEN_ERROR)

    user_token = UserRepository(session_=session).get_user_token(user_id)
    if user_token.access_token != token:
        Logger().error(
            f" 헤더의 토큰 값이 DB의 토큰값과 일치하지 않음. token: {token}, user_id: {user_id}"
        )
        raise InternalException(FailureType.UNAUTHORIZED_TOKEN_ERROR)

    return user_id
