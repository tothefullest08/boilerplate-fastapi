import re

from sqlalchemy.orm import Session

from src.common.auth import JwtTokenizer
from src.common.cipher import Cipher
from src.common.config import config
from src.common.exception import FailureType, InternalException
from src.common.logger import Logger
from src.user.interface.user_dto import JwtTokenDto, UserTokenDto
from src.user.model.user_model import UserModel
from src.user.repository.user_repository import UserRepository


class UserService:
    def __init__(self, session_: Session, logger: Logger = Logger()):
        self.__user_repo = UserRepository(session_=session_)
        self.__logger = logger

    def sign_in(self, phone_number: str, password: str) -> UserTokenDto:
        user = self.__validate_existing_user(phone_number)
        self.__verify_password(plain_password=password, hashed_password=user.password)

        jwt_token = self.__create_jwt_token(user_id=user.id)
        user_token = self.__user_repo.upsert_user_token(
            user_id=user.id,
            access_token=jwt_token.access_token,
            refresh_token=jwt_token.refresh_token,
        )

        return UserTokenDto(
            id=user_token.id,
            user_id=user_token.user_id,
            access_token=user_token.access_token,
            refresh_token=user_token.refresh_token,
            created_at=user_token.created_at,
            updated_at=user_token.updated_at,
        )

    def __validate_existing_user(self, phone_number: str) -> UserModel:
        user = self.__user_repo.get_user(phone_number=phone_number)
        if not user:
            raise InternalException(FailureType.NOT_AUTHORIZED_ERROR, "회원 정보가 없음")

        return user

    def __verify_password(self, plain_password: str, hashed_password: str) -> None:
        res = Cipher.verify(plain_password, hashed_password)
        if not res:
            raise InternalException(FailureType.NOT_AUTHORIZED_ERROR, "비밀번호 불일치")

    def sign_up(self, phone_number: str, password: str) -> UserTokenDto:
        self.__validate_phone_number(phone_number)
        self.__validate_new_user(phone_number)
        encrypted_password = self.__encrypt_password(password)
        user = self.__user_repo.create_user(
            phone_number=phone_number, password=encrypted_password
        )

        jwt_token = self.__create_jwt_token(user_id=user.id)
        user_token = self.__user_repo.upsert_user_token(
            user_id=user.id,
            access_token=jwt_token.access_token,
            refresh_token=jwt_token.refresh_token,
        )

        return UserTokenDto(
            id=user_token.id,
            user_id=user_token.user_id,
            access_token=user_token.access_token,
            refresh_token=user_token.refresh_token,
            created_at=user_token.created_at,
            updated_at=user_token.updated_at,
        )

    def __validate_phone_number(self, phone_number: str) -> None:
        pattern = re.compile("^010-[0-9]{4}-[0-9]{4}$")
        if not pattern.match(phone_number):
            raise InternalException(
                FailureType.INPUT_PARAMETER_ERROR, "전화번호 양식이 잘못되었습니다."
            )

    def __validate_new_user(self, phone_number: str) -> None:
        user = self.__user_repo.get_user(phone_number=phone_number)
        if user:
            raise InternalException(FailureType.NOT_AUTHORIZED_ERROR, "이미 유저 정보가 존재함")

    def __encrypt_password(self, password: str) -> str:
        return Cipher.encrypt(password)

    def sign_out(self, user_id: int) -> None:
        self.__user_repo.delete_user_token(user_id)

    def __create_jwt_token(
        self,
        user_id: int,
    ) -> JwtTokenDto:
        access_token = JwtTokenizer.encode(
            payload={
                "user_id": user_id,
                "sub": "access_token",
            },
            token_expire_minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES,
            key=config.ACCESS_TOKEN_SECRET,
        )

        refresh_token = JwtTokenizer.encode(
            payload={
                "user_id": user_id,
                "sub": "refresh_token",
            },
            token_expire_minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES,
            key=config.REFRESH_TOKEN_SECRET,
        )

        return JwtTokenDto(access_token=access_token, refresh_token=refresh_token)
