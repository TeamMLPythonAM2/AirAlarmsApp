from pydantic import BaseModel
from shared.RequestService import RequestService
import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')
API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"


class WeatherHour(BaseModel):
    location: str
    datetime: str
    temp: float
    windspeed: float
    winddir: float
    precip: float
    humidity: float
    pressure: float
    cloudcover: float

    def __str__(self):
        return (f"location: {self.location}\n"
                f"latetime: {self.datetime}\n"
                f"lemperature: {self.temp}°\n"
                f"wind speed: {self.windspeed} km/h\n"
                f"wind direction: {self.winddir}°\n"
                f"precipitation: {self.precip} mm\n"
                f"humidity: {self.humidity}%\n"
                f"pressure: {self.pressure} hPa\n"
                f"cloud cover: {self.cloudcover}%")
# hour weather object


class WeatherService(RequestService[list[WeatherHour]]):
    @staticmethod
    def request(location="Kyiv", unit_group="metric") -> list[WeatherHour]:
        params = {
            "key": API_KEY,
            "unitGroup": unit_group,
            "location": location,
            "include": "hours"
        }

        response = requests.get(API_URL, params=params).json()

        daily_data = response['days'][0]['hours']
        hours_list = []

        for hour in daily_data:
            hourly_data = WeatherHour.model_validate(
                {"location": location, **hour}
            )

            hours_list.append(hourly_data)

        return hours_list
# weather service


# test_today_weather = WeatherService.request()
#
# print(test_today_weather[2])
