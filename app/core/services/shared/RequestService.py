from typing import TypeVar, Generic, Type, NamedTuple
from abc import ABC, abstractmethod

DataType = TypeVar('DataType', bound=NamedTuple)


class RequestService(ABC, Generic[DataType]):
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
