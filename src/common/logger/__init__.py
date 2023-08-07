import logging
import sys
import time

from src.common.config import config


class BaseSingleton(type):
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(BaseSingleton, cls).__call__(*args, **kwargs)
        return cls._inst[cls]


class Logger(metaclass=BaseSingleton):
    def __init__(self):
        logging.basicConfig(stream=sys.stdout)
        logging.Formatter.converter = time.gmtime

        self._logger = logging.getLogger(config.SERVICE_NAME)
        self._logger.setLevel(20)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)

    def debug(self, msg: str):
        self._logger.debug(msg)

    def info(self, msg: str):
        self._logger.info(msg)

    def warning(self, msg: str):
        self._logger.warning(msg)

    def error(self, msg: str):
        self._logger.error(msg)
