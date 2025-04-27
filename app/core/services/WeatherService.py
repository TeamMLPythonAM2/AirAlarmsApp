from app.config.configuration import Config
from app.core.entities.WeatherDTO import WeatherDTO
from app.core.services.shared.ABRequestService import ABRequestService
import aiohttp
import datetime as dt


class WeatherService(ABRequestService[list[WeatherDTO]]):
    @staticmethod
    async def request(location: str="Kyiv", now: bool=False, unit_group: str="metric") -> list[WeatherDTO]:
        params = {
            "key": Config.WEATHER_API_KEY,
            "unitGroup": unit_group,
            "location": location + ' UA',
            "include": "hours"
        }

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(Config.WEATHER_API_URL, params=params) as resp:
                response = await resp.json()
        # response: json

        data = response['days'][0]['hours']

        if now:
            data = []
            now_dt = dt.datetime.now(tz=Config.KYIV_TZ).replace(minute=0, second=0, microsecond=0)
            end_dt = now_dt + dt.timedelta(hours=24)

            for day in response['days'][:2]:
                for hour in day['hours']:
                    full_dt = dt.datetime.strptime(
                        f"{day['datetime']} {hour['datetime']}",
                        "%Y-%m-%d %H:%M:%S"
                    ).replace(tzinfo=Config.KYIV_TZ)
                    if now_dt <= full_dt < end_dt:
                        hour['datetime'] = full_dt
                        hour['day_temp'] = day['temp']
                        hour['day_humidity'] = day['humidity']
                        hour['day_dew'] = day['dew']
                        hour['day_precipcover'] = day['precipcover']
                        hour['day_precip'] = day['precip']
                        data.append(hour)

        hours_list = []
        for hour in data:
            mapped_hour = {
                "datetime": hour["datetime"],
                "hour_temp": hour["temp"],
                "hour_windspeed": hour["windspeed"],
                "hour_winddir": hour["winddir"],
                "hour_precip": hour["precip"],
                "hour_humidity": hour["humidity"],
                "hour_pressure": hour["pressure"],
                "hour_cloudcover": hour["cloudcover"],
                "hour_visibility": hour["visibility"],
                "hour_windgust": hour["windgust"],
                "hour_solarenergy": hour["solarenergy"],
                "hour_snow": hour["snow"],
                "hour_dew": hour["dew"],
                "day_temp": hour["day_temp"],
                "day_humidity": hour["day_humidity"],
                "day_dew": hour["day_dew"],
                "day_precipcover": hour["day_precipcover"],
                "day_precip": hour["day_precip"],
            }
            hourly_data = WeatherDTO(city_address=location, **mapped_hour)
            hours_list.append(hourly_data)

        return hours_list
