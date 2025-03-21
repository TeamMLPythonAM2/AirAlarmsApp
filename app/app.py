from config import *
from core.services.ExampleService import ExampleService, WeatherDTO

CONFIG = Config()

secret = CONFIG.TEST_SECRET

data = ExampleService.to_dict(ExampleService.request())
print(data)
print(ExampleService.from_dict(data, WeatherDTO))
