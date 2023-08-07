from sqlalchemy.orm import Session

from src.common.exception import InternalException, FailureType
from src.common.logger import Logger
from src.user.model.user_model import UserModel


class UserRepository:
    def __init__(self, session: Session, logger: Logger = Logger()):
        self.__session = session
        self.__logger = logger

    def get_users(self) -> [UserModel]:
        try:
            return self.__session.query(UserModel).all()
        except Exception as e:
            self.__logger.error(f"유저 목록 조회 실패, e: {e}")
            raise InternalException(FailureType.GET_DATA_ERROR, "유저 목록 조회 실패")
