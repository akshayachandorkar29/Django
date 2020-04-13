import redis
import logging
logging.basicConfig(level=logging.DEBUG)
from django.conf import settings


class RedisService:
    def __init__(self, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, ):
        self.host = host
        self.port = port
        self.db = db
        self.connection = self.connect()

    def connect(self):
        connection = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
        if connection:
            logging.info('Redis Cache Connection established')
        return connection

    def set(self, key, value, exp_s=None, exp_ms=None):
        self.connection.set(key, value, exp_s, exp_ms)
        logging.info(f'{key} : {value}')

    def get(self, key):
        return self.connection.get(key)

    def exists(self, key):
        return self.connection.exists(key)

    def delete(self, key):
        logging.info(f'Key to Delete : {key}')
        self.connection.delete(key)