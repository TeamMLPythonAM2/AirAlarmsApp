import asyncio
import json
import os.path
from datetime import datetime

from app.core.scrapers.web_scraper.isw_enum import ISWEnum
from app.core.scrapers.web_scraper.isw_scraper import ISWScraper
from app.core.scrapers.web_scraper.web_parser.isw_parser import ISWParser

from app.config.configuration import Config


async def update_isw_reports():
    month = (today := datetime.now()).strftime("%B")
    day = today.day
    year = today.year
    for i in range(day, day - 2, -1):
        file_name = f"{month.lower()}_{i}.html.gz"
        if os.path.exists(os.path.join(Config.FULL_REPORTS_PATH, str(year), file_name)):
            return

    file_name = ISWEnum.REPORTS_2025.name
    last_link, last_date = None, None

    if os.path.exists((path := os.path.join(Config.LINKS_PATH, file_name + ".json"))):
        with open(path, "r") as json_file:
            data: dict[str, str] = json.load(json_file)
            last_link = data[(last_date := list(data)[0])]
            json_file.close()

    await ISWScraper.get_page_content(
        full_url=ISWEnum.REPORTS_2025,
        file_name=file_name,
        path=Config.SHORT_REPORTS_PATH,
    )

    isw_parser = ISWParser()
    await isw_parser.parse_href(
        file_name=file_name,
        path=Config.SHORT_REPORTS_PATH
    )

    await isw_parser.upload_from_hrefs(path=Config.LINKS_PATH)
    with open(os.path.join(Config.LINKS_PATH, file_name + ".json"), "r") as json_file:
        data: dict[str, str] = json.load(json_file)
        json_file.close()
    for date, link in data.items():
        if date == last_date and link == last_link:
            break
        await ISWScraper.get_page_content(
            full_url=link,
            file_name=date,
            path=os.path.join(Config.FULL_REPORTS_PATH, "2025"),
        )


if __name__ == "__main__":
    asyncio.run(update_isw_reports())
