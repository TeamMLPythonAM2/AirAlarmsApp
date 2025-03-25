from dotenv import load_dotenv
from os import environ
import os

ROOT_PATH = './../.env'
load_dotenv()


class Config:
    TEST_SECRET = environ.get('TEST_SECRET')
    ALARMS_API_KEY = os.environ.get("ALARMS_API_KEY")
    LIST_OF_REGIONS_URL = "https://api.ukrainealarm.com/api/v3/regions"
    AIR_URL = "https://api.ukrainealarm.com/api/v3/alerts"
    # WEBHOOK_URL = "https://api.ukrainealarm.com/api/v3/webhook"

    EXCLUDED_REGIONS = {
        "Тестовий регіон", "Луганська область", "Автономна Республіка Крим"
    }
