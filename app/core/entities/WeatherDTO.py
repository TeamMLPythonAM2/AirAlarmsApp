from pydantic import BaseModel
import datetime as dt


class WeatherDTO(BaseModel):
    city_address: str
    datetime: dt.datetime
    hour_temp: float
    hour_windspeed: float
    hour_winddir: float
    hour_precip: float
    hour_humidity: float
    hour_pressure: float
    hour_cloudcover: float
    hour_visibility: float
    hour_windgust: float
    hour_solarenergy: float
    hour_snow: float
    hour_dew: float
    day_temp: float
    day_humidity: float
    day_dew: float
    day_precipcover: float
    day_precip: float

    def __str__(self):
        return (f"city_address: {self.city_address}\n"
                f"datetime: {self.datetime}\n"
                f"hour_temp: {self.hour_temp}°\n"
                f"hour_windspeed: {self.hour_windspeed} km/h\n"
                f"hour_winddir: {self.hour_winddir}°\n"
                f"precip: {self.hour_precip} mm\n"
                f"hour_humidity: {self.hour_humidity}%\n"
                f"hour_pressure: {self.hour_pressure} hPa\n"
                f"hour_cloudcover: {self.hour_cloudcover}%\n"
                f"hour_visibility: {self.hour_visibility} km\n"
                f"hour_windgust: {self.hour_windgust} km/h\n"
                f"hour_solarenergy: {self.hour_solarenergy} MJ/m²\n"
                f"hour_snow: {self.hour_snow} mm\n"
                f"hour_dew: {self.hour_dew}°\n"
                f"day_temp: {self.day_temp}°\n"
                f"day_humidity: {self.day_humidity}%\n"
                f"day_dew: {self.day_dew}°\n"
                f"day_precipcover: {self.day_precipcover}%\n"
                f"day_precip: {self.day_precip} mm")
