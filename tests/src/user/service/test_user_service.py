import pytest
from starlette.testclient import TestClient

from src.common.cipher import Cipher
from src.common.exception import InternalException
from src.user.interface.user_dto import UserTokenDto
from src.user.repository.user_repository import UserRepository
from src.user.service.user_service import UserService


def test_sign_in_should_return_user_token_dto(
    test_session, generate_random_phone_numer
):
    # Given
    phone_number = generate_random_phone_numer
    password = "password"
    UserRepository(session_=test_session).create_user(
        phone_number=phone_number, password=Cipher.encrypt(password)
    )

    # When
    user_token = UserService(session_=test_session).sign_in(
        phone_number=phone_number, password=password
    )

    # Then
    assert isinstance(user_token, UserTokenDto)
    user = UserRepository(session_=test_session).get_user(phone_number=phone_number)
    assert user is not None
    user_token = UserRepository(session_=test_session).get_user_token(user.id)
    assert user_token is not None


def test_sign_in_should_raise_internal_error_when_password_is_not_valid(
    test_session, generate_random_phone_numer
):
    # Given
    phone_number = generate_random_phone_numer
    password = "password"
    UserRepository(session_=test_session).create_user(
        phone_number=phone_number, password=Cipher.encrypt(password)
    )

    # When & Then
    with pytest.raises(InternalException):
        UserService(session_=test_session).sign_in(
            phone_number=phone_number, password=password + "dummy"
        )


def test_sign_up_should_return_user_token_dto(
    test_session, generate_random_phone_numer
):
    # Given
    phone_number = generate_random_phone_numer
    password = "password"

    # When
    user_token = UserService(session_=test_session).sign_up(
        phone_number=phone_number, password=password
    )

    # Then
    assert isinstance(user_token, UserTokenDto)
    user = UserRepository(session_=test_session).get_user(phone_number=phone_number)
    assert user is not None
    user_token = UserRepository(session_=test_session).get_user_token(user.id)
    assert user_token is not None


def test_sign_up_should_raise_internal_error_when_phone_number_is_not_valid(
    test_session,
):
    # Given
    phone_number = "010-12-5678"
    password = "password"

    # When & Then
    with pytest.raises(InternalException):
        UserService(session_=test_session).sign_up(
            phone_number=phone_number, password=password
        )


def test_sign_up_should_raise_error_when_user_already_exist(
    client: TestClient, test_session, generate_random_phone_numer
):
    # Given
    phone_number = generate_random_phone_numer
    password = "password"
    UserRepository(session_=test_session).create_user(
        phone_number=phone_number, password="sample"
    )
    # When & Then
    with pytest.raises(InternalException):
        UserService(session_=test_session).sign_up(
            phone_number=phone_number, password=password
        )


def test_sign_out_should_delete_user_token(test_session, generate_random_phone_numer):
    # Given
    phone_number = generate_random_phone_numer
    password = "password"
    user_token = UserService(session_=test_session).sign_up(
        phone_number=phone_number, password=password
    )

    # When
    UserService(session_=test_session).sign_out(user_token.user_id)

    # Then
    user_token = UserRepository(session_=test_session).get_user_token(
        user_token.user_id
    )
    assert user_token is None
