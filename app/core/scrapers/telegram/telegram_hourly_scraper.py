import datetime as dt
import pytz
from app.core.scrapers.telegram.telegram_scraper import TelegramScraper


async def update_messages() -> dt.datetime:
    kyiv_tz = pytz.timezone("Europe/Kyiv")
    date = dt.datetime.now(tz=kyiv_tz).replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=1)

    await TelegramScraper.scrape_content(date)

    return date
