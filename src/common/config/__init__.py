import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    SERVICE_NAME: str = "boiler_plate"
    APP_HOST: str = "localhost"
    APP_PORT: int = 7002
    WRITER_DB_URL: str = (
        "mysql+pymysql://admin:admin1234@localhost:33060/mysql"
    )
    READER_DB_URL: str = (
        "mysql+pymysql://admin:admin1234@localhost:33060/mysql"
    )


class LocalConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "local": LocalConfig(),
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
