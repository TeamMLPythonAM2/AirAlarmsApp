from abc import ABC, abstractmethod
from pydantic import BaseModel


class ABRequestService[DataType: BaseModel](ABC):
    @staticmethod
    @abstractmethod
    def request() -> DataType:
        pass
