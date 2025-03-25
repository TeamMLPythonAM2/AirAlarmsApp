from pydantic import BaseModel


class WeatherDTO(BaseModel):
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
