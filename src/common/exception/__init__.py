from src.common.exception.failure_type import FailureType


class InternalException(Exception):
    def __init__(
        self,
        _failure_type: FailureType,
        _description: str = "",
    ):
        self.__failure_type = _failure_type
        self.__description = _description

    def get_description(self):
        return self.__description

    def get_error_type(self):
        return self.__failure_type.error_type

    def get_status_code(self):
        return self.__failure_type.status_code
