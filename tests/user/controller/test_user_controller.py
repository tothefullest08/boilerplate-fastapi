from starlette.testclient import TestClient

from src.common.cipher import Cipher
from src.user.repository.user_repository import UserRepository


def test_sign_in_e2e_should_return_200(client: TestClient, test_session):
    # Given
    phone_number = "010-1234-5678"
    password = "password"
    UserRepository(session_=test_session).create_user(
        phone_number="010-1234-5678", password=Cipher.encrypt(password)
    )
    data = {
        "phone_number": phone_number,
        "password": password,
    }

    # When
    response = client.post(f"api/v1/users/sign-in", json=data)

    # Then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"] is not None

    user = UserRepository(session_=test_session).get_user(phone_number="010-1234-5678")
    assert user is not None
    user_token = UserRepository(session_=test_session).get_user_token(user.id)
    assert user_token is not None


def test_sign_in_e2e_should_return_401_when_password_is_not_valid(
    client: TestClient, test_session
):
    # Given
    phone_number = "010-1234-5678"
    password = "password"
    UserRepository(session_=test_session).create_user(
        phone_number="010-1234-5678", password=Cipher.encrypt(password)
    )
    data = {
        "phone_number": phone_number,
        "password": password + "dummy",
    }

    # When
    response = client.post(f"api/v1/users/sign-in", json=data)

    # Then
    assert response.status_code == 401
    assert response.json()["meta"]["code"] == 401
    assert response.json()["meta"]["message"] is not None
    assert response.json()["data"] is None


def test_sign_up_e2e_should_return_200(client: TestClient, test_session):
    # Given
    data = {
        "phone_number": "010-1234-5678",
        "password": "password",
    }

    # When
    response = client.post(f"api/v1/users/sign-up", json=data)

    # Then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"
    assert response.json()["data"] is not None

    user = UserRepository(session_=test_session).get_user(phone_number="010-1234-5678")
    assert user is not None
    user_token = UserRepository(session_=test_session).get_user_token(user.id)
    assert user_token is not None


def test_sign_up_e2e_should_return_400_when_phone_number_is_not_valid(
    client: TestClient, test_session
):
    # Given
    data = {
        "phone_number": "010-12-5678",
        "password": "password",
    }

    # When
    response = client.post(f"api/v1/users/sign-up", json=data)

    # Then
    assert response.status_code == 400
    assert response.json()["meta"]["code"] == 400
    assert response.json()["meta"]["message"] is not None
    assert response.json()["data"] is None


def test_sign_up_e2e_should_return_400_when_user_already_exist(
    client: TestClient, test_session
):
    # Given
    UserRepository(session_=test_session).create_user(
        phone_number="010-1234-5678", password="sample"
    )
    data = {
        "phone_number": "010-1234-5678",
        "password": "password",
    }

    # When
    response = client.post(f"api/v1/users/sign-up", json=data)

    # Then
    assert response.status_code == 401
    assert response.json()["meta"]["code"] == 401
    assert response.json()["meta"]["message"] is not None
    assert response.json()["data"] is None
