import asyncio
import datetime as dt

from app.core.scrapers.telegram.telegram_scraper import TelegramScraper


async def update_telegram_messages():
    start_date = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + dt.timedelta(days=1)

    await TelegramScraper.scrape_content(start_date, end_date)


if __name__ == "__main__":
    asyncio.run(update_telegram_messages())
