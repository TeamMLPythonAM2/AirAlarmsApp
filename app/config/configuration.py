from dotenv import load_dotenv
from os import environ

load_dotenv()


class Config:
    WEATHER_API_KEY = environ.get('WEATHER_API_KEY')
    WEATHER_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

