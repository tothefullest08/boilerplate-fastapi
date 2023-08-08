from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from src.common.config import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
