import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from pydantic import StringConstraints

load_dotenv()


class Config:
    # air alarms api
    # WEBHOOK_URL = "https://api.ukrainealarm.com/api/v3/webhook"
    ALARMS_API_KEY = os.environ.get("ALARMS_API_KEY")
    LIST_OF_REGIONS_URL = "https://api.ukrainealarm.com/api/v3/regions"
    AIR_URL = "https://api.ukrainealarm.com/api/v3/alerts"
    EXCLUDED_REGIONS = {
        "Тестовий регіон", "Луганська область", "Автономна Республіка Крим"
    }
    # weather api
    WEATHER_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')

    FILES_PATH = os.path.join(Path(__file__).resolve().parents[2], "files")

    # ISW parser
    SHORT_REPORTS_PATH = os.path.join(
        FILES_PATH, "isw_reports", "short_reports"
    )
    FULL_REPORTS_PATH = os.path.join(
        FILES_PATH, "isw_reports", "full_reports"
    )
    LINKS_PATH = os.path.join(
        FILES_PATH, "isw_reports", "links"
    )
    URL_PATTERN = Annotated[str, StringConstraints(pattern=r"https?://[-.a-zA-Z]{1,}")]
    # telegram parser
    TELEGRAM_MESSAGES_PATH = os.path.join(FILES_PATH, 'telegram_messages')
    TELEGRAM_API_ID: int = os.environ.get('TELEGRAM_API_ID')
    TELEGRAM_API_HASH: str = os.environ.get('TELEGRAM_API_HASH')
    TELEGRAM_API_PHONE: str = os.environ.get('TELEGRAM_API_PHONE')
