import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    SERVICE_NAME: str = "boiler_plate"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = "mysql+pymysql://root:fastapi@localhost:3306/fastapi"
    READER_DB_URL: str = "mysql+pymysql://root:fastapi@localhost:3306/fastapi"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_SECRET: str = "secret1234"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_SECRET: str = "refresh_secret1234"
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 20160


class LocalConfig(Config):
    pass


class TestingConfig(Config):
    WRITER_DB_URL: str = "sqlite:///test.db"
    READER_DB_URL: str = "sqlite:///test.db"


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = "mysql+pymysql://root:fastapi@db:3306/fastapi"
    READER_DB_URL: str = "mysql+pymysql://root:fastapi@db:3306/fastapi"


class ProductionConfig(Config):
    pass


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "local": LocalConfig(),
        "testing": TestingConfig(),
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
