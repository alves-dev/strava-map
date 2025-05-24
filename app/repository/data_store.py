from abc import ABC, abstractmethod


class DataStore(ABC):

    @classmethod
    @abstractmethod
    def add(cls, key: str, value: str):
        """Deve salvar um valor em str a partir da chave"""
        pass

    @classmethod
    @abstractmethod
    def get(cls, key: str) -> str:
        """Recupera o valor str a partir da chave"""
        pass

    @classmethod
    @abstractmethod
    def add_json(cls, key: str, value: dict):
        """Deve salvar um dict a partir da chave"""
        pass

    @classmethod
    @abstractmethod
    def get_json(cls, key: str) -> dict:
        """Recupera um dict a partir da chave"""
        pass
