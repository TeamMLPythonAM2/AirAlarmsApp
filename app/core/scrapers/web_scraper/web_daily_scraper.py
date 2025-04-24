import asyncio
import json
import os.path
from datetime import datetime

import pandas as pd

from app.core.scrapers.web_scraper.isw_enum import ISWEnum
from app.core.scrapers.web_scraper.isw_scraper import ISWScraper

from app.config.configuration import Config


async def update_isw_reports():
    today = datetime.now().isocalendar()
    df = pd.read_parquet(Config.ISW_PARQUET_PATH)
    last_update = df["date"].aggregate("max").isocalendar()
    if today <= last_update:
        return
    cont = []





if __name__ == "__main__":
    asyncio.run(update_isw_reports())
