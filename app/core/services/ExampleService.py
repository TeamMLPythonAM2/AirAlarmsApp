from typing import NamedTuple

from pydantic import BaseModel

from .shared.ABRequestService import ABRequestService

# must be in entities folder, here just for an example
class WeatherDTO(BaseModel):
    prp: str
    ppp: str


class ExampleService(ABRequestService[WeatherDTO]):
    @staticmethod
    def request() -> WeatherDTO:
        # request logic
        return WeatherDTO(**{"prp": "", "ppp": ""})
