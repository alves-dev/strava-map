from app.config.setting import setting
from app.repository.data_store import DataStore
from app.repository.store_redis import DataStoreRedis


def get_store() -> DataStore:
    return DataStoreRedis(host=setting.REDIS_HOST, port=setting.REDIS_PORT, username=setting.REDIS_USERNAME,
                          password=setting.REDIS_PASSWORD)
