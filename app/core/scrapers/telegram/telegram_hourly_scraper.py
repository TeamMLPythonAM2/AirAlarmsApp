import datetime as dt
from app.core.scrapers.telegram.telegram_scraper import TelegramScraper
from app.config.configuration import Config


async def update_messages() -> dt.datetime:
    date = dt.datetime.now(tz=Config.KYIV_TZ).replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=1)

    await TelegramScraper.scrape_content(date)

    return date
