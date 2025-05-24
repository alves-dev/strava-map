import json

import redis

from app.repository.data_store import DataStore


class DataStoreRedis(DataStore):
    def __init__(self, host='localhost', port=6379, username=None, password=None, db=0):
        self.prefix = 'strava-map:'
        self.client = redis.Redis(
            host=host,
            port=port,
            username=username,
            password=password,
            db=db,
            decode_responses=True  # pra receber strings em vez de bytes
        )

    def add(self, key: str, value: str):
        self.client.set(f'{self.prefix}{key}', value)

    def get(self, key: str):
        return self.client.get(f'{self.prefix}{key}')

    def add_json(self, key: str, value: dict):
        json_value = json.dumps(value)
        self.client.set(f'{self.prefix}{key}', json_value)

    def get_json(self, key: str) -> dict:
        value = self.client.get(f'{self.prefix}{key}')
        if value:
            return json.loads(value)
        return {}
