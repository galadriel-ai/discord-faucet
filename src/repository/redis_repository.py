from typing import Optional
from typing import Union

import redis

import settings
from src import api_logger

logger = api_logger.get()


class RedisRepository:

    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT
        )

    def set(self, key: str, value: Union[str, int]):
        try:
            self.client.set(key, value)
        except Exception as e:
            logger.error(e, exc_info=True)

    def get_numeric(self, key: str) -> Optional[int]:
        try:
            value = self.client.get(key)
            if value:
                return int(value.decode())
        except Exception as e:
            logger.error(e, exc_info=True)
            return None
