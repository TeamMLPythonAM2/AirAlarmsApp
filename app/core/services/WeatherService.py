from app.config.configuration import Config
from app.core.entities.WeatherDTO import WeatherDTO
from app.core.services.shared.ABRequestService import ABRequestService
import aiohttp


class WeatherService(ABRequestService[list[WeatherDTO]]):
    @staticmethod
    async def request(location="Kyiv", unit_group="metric") -> list[WeatherDTO]:
        params = {
            "key": Config.WEATHER_API_KEY,
            "unitGroup": unit_group,
            "location": location,
            "include": "hours"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(Config.WEATHER_API_URL, params=params) as resp:
                response = await resp.json()
        # response: json

        daily_data = response['days'][0]['hours']
        hours_list = []

        for hour in daily_data:
            hourly_data = WeatherDTO(location=location, **hour)
            hours_list.append(hourly_data)

        return hours_list
