import asyncio
import gzip
import os

import aiohttp
from pydantic import validate_call

from app.core.scrapers.web_scraper.consts import FILES_PATH, URL_PATTERN
from app.core.scrapers.web_scraper.isw_enum import ISWEnum


class ISWScraper:

    @classmethod
    @validate_call
    async def get_page_content(cls, full_url: URL_PATTERN, file_name: str):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.get(full_url) as response:
                html = await response.text()
                compressed_html = gzip.compress(html.encode("utf-8"))
                with open(
                    os.path.join(FILES_PATH, file_name + ".html.gz"), "wb"
                ) as file:
                    file.write(compressed_html)


if __name__ == "__main__":
    for i in ISWEnum:
        asyncio.run(ISWScraper.get_page_content(i, i.name))
