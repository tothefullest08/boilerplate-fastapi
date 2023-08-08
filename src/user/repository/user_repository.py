from typing import List, Union
from sqlalchemy.orm import Session
from src.common.exception import InternalException, FailureType
from src.common.logger import Logger
from src.user.model.user_model import UserModel, UserTokenModel


class UserRepository:
    def __init__(self, session_: Session, logger: Logger = Logger()):
        self.__session = session_
        self.__logger = logger

    def create_user(self, phone_number: str, password: str) -> UserTokenModel:
        try:
            user: UserModel = UserModel(
                phone_number=phone_number,
                password=password,
            )
            self.__session.add(user)
            self.__session.commit()

            return user

        except Exception as e:
            self.__session.rollback()
            self.__session.flush()

            self.__logger.error(f" 유저 생성 실패. phone_number: {phone_number}, e: {e}")
            raise InternalException(FailureType.CREATE_DATA_ERROR, "유저 생성 실패")

    def get_users(
        self, user_ids: List[int] = None, phone_number: str = None
    ) -> List[UserModel]:
        try:
            filter_ = []
            if user_ids:
                filter_.append(UserModel.user_id.in_(user_ids))
            if phone_number:
                filter_.append(UserModel.phone_number == phone_number)

            return self.__session.query(UserModel).filter(*filter_).all()
        except Exception as e:
            self.__logger.error(f"유저 목록 조회 실패, user_ids: {user_ids}, e: {e}")
            raise InternalException(FailureType.GET_DATA_ERROR, "유저 목록 조회 실패")

    def get_user(
        self, user_id: int = None, phone_number: str = None
    ) -> Union[UserModel, None]:
        user_ids = [user_id] if user_id else None
        users = self.get_users(user_ids=user_ids, phone_number=phone_number)
        if not users:
            return None
        return users[0]

    def upsert_user_token(
        self, user_id: int, access_token: int, refresh_token: int
    ) -> UserTokenModel:
        try:
            user_token = (
                self.__session.query(UserTokenModel)
                .filter(UserTokenModel.user_id == user_id)
                .first()
            )
            if user_token:
                user_token.access_token = access_token
                user_token.refresh_token = refresh_token

            else:
                user_token: UserTokenModel = UserTokenModel(
                    user_id=user_id,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )
            self.__session.add(user_token)
            self.__session.commit()

            return user_token

        except Exception as e:
            self.__session.rollback()
            self.__session.flush()

            self.__logger.error(f" 유저 토큰 upsert 실패. user_id: {user_id}, e: {e}")
            raise InternalException(FailureType.UPSERT_DATA_ERROR, "유저 토큰 upsert 실패")

    def get_user_token(self, user_id: int = None) -> Union[UserTokenModel, None]:
        try:
            return (
                self.__session.query(UserTokenModel)
                .filter(UserTokenModel.user_id == user_id)
                .first()
            )
        except Exception as e:
            self.__logger.error(f"유저 토큰 조회 실패, user_id: {user_id}, e: {e}")
            raise InternalException(FailureType.GET_DATA_ERROR, "유저 토큰 조회 실패")

    def delete_user_token(self, user_id: int) -> None:
        try:
            removed_count = (
                self.__session.query(UserTokenModel)
                .filter(UserTokenModel.user_id == user_id)
                .delete(synchronize_session="fetch")
            )
            if not removed_count:
                self.__session.flush()
                return 0

            self.__session.commit()

            return removed_count

        except Exception as e:
            self.__session.rollback()
            self.__session.flush()
            self.__logger.error(f" 유저 토큰 삭제 실패. user_id: {user_id}, e: {e}")
            raise InternalException(FailureType.DELETE_DATA_ERROR, "유저 토큰 삭제 실패")
