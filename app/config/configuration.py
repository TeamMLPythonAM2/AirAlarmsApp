import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from pydantic import StringConstraints

load_dotenv()


class Config:
    WEATHER_API_KEY = environ.get('WEATHER_API_KEY')
    WEATHER_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    SHORT_REPORTS_PATH = os.path.join(
        Path(__file__).resolve().parents[2], "files", "isw_reports", "short_reports"
    )
    FULL_REPORTS_PATH = os.path.join(
        Path(__file__).resolve().parents[2], "files", "isw_reports", "full_reports"
    )
    LINKS_PATH = os.path.join(
        Path(__file__).resolve().parents[2], "files", "isw_reports", "links"
    )
    URL_PATTERN = Annotated[str, StringConstraints(pattern=r"https?://[-.a-zA-Z]{1,}")]
