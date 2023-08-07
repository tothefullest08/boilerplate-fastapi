from typing import List

from sqlalchemy.orm import Session

from src.user.model.user_model import UserModel
from src.user.repository.user_repository import UserRepository


class UserService:
    def __init__(self, session: Session):
        self.__session = session
        self.__user_repo = UserRepository(session=session)

    def get_users(self) -> List[UserModel]:
        return self.__user_repo.get_users()

    def sign_in(self):
        pass

    def sign_up(self):
        pass

    def sign_out(self):
        pass
