from redis import StrictRedis
from config import ConfigClass
from commons.logger_services.logger_factory_service import SrvLoggerFactory

_logger = SrvLoggerFactory('SrvRedisSingleton').get_logger()


class SrvRedisSingleton():
    __instance = {}

    def __init__(self):
        self.host = ConfigClass.REDIS_HOST
        self.port = ConfigClass.REDIS_PORT
        self.db = ConfigClass.REDIS_DB
        self.pwd = ConfigClass.REDIS_PASSWORD
        self.connect()

    def connect(self):
        if self.__instance:
            pass
        else:
            self.__instance = StrictRedis(host=self.host,
                                          port=self.port,
                                          db=self.db,
                                          password=self.pwd)


    def mget_by_prefix(self, prefix: str):
        _logger.debug(prefix)
        query = '{}:*'.format(prefix)
        keys = self.__instance.keys(query)
        return self.__instance.mget(keys)

    def get_by_prefix(self, prefix: str):
        _logger.debug(prefix)
        query = '*:{}:*'.format(prefix)
        keys = self.__instance.keys(query)
        return keys

    def delete_by_key(self, key: str):
        return self.__instance.delete(key)


