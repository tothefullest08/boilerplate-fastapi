from passlib.context import CryptContext


class Cipher:
    @staticmethod
    def verify(plain_value: str, hashed_value: str):
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(
            plain_value, hashed_value
        )

    @staticmethod
    def encrypt(plain_value: str):
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(plain_value)
