from typing import NamedTuple
from .shared.RequestService import RequestService


# must be in entities folder, here just for an example
class WeatherDTO(NamedTuple):
    prp: str
    ppp: str


class ExampleService(RequestService[WeatherDTO]):
    @staticmethod
    def request() -> WeatherDTO:
        # request logic
        return WeatherDTO(**{"prp": "", "ppp": ""})
