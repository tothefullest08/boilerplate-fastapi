from enum import Enum


class FailureType(Enum):
    INPUT_PARAMETER_ERROR = ("input_parameter_error", 400)
    INVALID_REQUEST_ERROR = ("invalid_request_error", 400)
    CREATE_DATA_ERROR = ("create_data_error", 400)
    GET_DATA_ERROR = ("get_data_error", 400)
    UPSERT_DATA_ERROR = ("upsert_data_error", 400)
    UPDATE_DATA_ERROR = ("update_data_error", 400)
    DELETE_DATA_ERROR = ("delete_data_error", 400)
    DATA_PROCESSING_ERROR = ("data_processing_error", 400)
    NOT_FOUND_ERROR = ("not_found_error", 400)
    NOT_AUTHORIZED_ERROR = ("not_authorized_error", 401)
    UNAUTHORIZED_TOKEN_ERROR = ("unauthorized_token_error", 401)

    @property
    def error_type(self) -> str:
        return self.value[0]

    @property
    def status_code(self) -> int:
        return self.value[1]
