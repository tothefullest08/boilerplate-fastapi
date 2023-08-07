from src.common.exception import InternalException, FailureType


class AuthValidator:
    @staticmethod
    def validate_user_token(user_token: str = None) -> bool:
        # TODO : validation 로직 고도화 필요
        if not user_token:
            raise InternalException(FailureType.NOT_AUTHORIZED_ERROR, "유저 토큰 없음")

        return True
