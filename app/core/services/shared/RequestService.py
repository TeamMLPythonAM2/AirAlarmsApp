from abc import ABC, abstractmethod
from typing import NamedTuple, Type


class RequestService[DataType: NamedTuple](ABC):
    @staticmethod
    def to_dict(data: DataType) -> dict:
        return data._asdict()

    @classmethod
    def from_dict(cls, data: dict, entity_type: Type[DataType]) -> DataType:
        return entity_type(**data)

    @staticmethod
    @abstractmethod
    def request() -> DataType:
        pass
