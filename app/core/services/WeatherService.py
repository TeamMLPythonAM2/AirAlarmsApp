from app.core.consts import WEATHER_API_KEY, WEATHER_API_URL
from app.core.entities.WeatherDTO import WeatherDTO
from shared.ABRequestService import ABRequestService
import requests


class WeatherService(ABRequestService[list[WeatherDTO]]):
    @staticmethod
    def request(location="Kyiv", unit_group="metric") -> list[WeatherDTO]:
        params = {
            "key": WEATHER_API_KEY,
            "unitGroup": unit_group,
            "location": location,
            "include": "hours"
        }

        response: requests.Response = requests.get(WEATHER_API_URL, params=params)
        # validation
        response: dict = response.json()

        daily_data = response['days'][0]['hours']
        hours_list = []

        for hour in daily_data:
            hourly_data = WeatherDTO(location=location, **hour)
            hours_list.append(hourly_data)

        return hours_list


if __name__ == "__main__":
    # weather service
    test_today_weather = WeatherService.request()
    print(test_today_weather[2])
