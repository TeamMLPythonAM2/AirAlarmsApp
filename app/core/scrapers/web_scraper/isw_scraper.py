import gzip
import os

import aiohttp
from pydantic import validate_call

from app.config.configuration import Config


class ISWScraper:

    @classmethod
    @validate_call
    async def get_page_content(
        cls, full_url: Config.URL_PATTERN, file_name: str, path: str
    ):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.get(full_url) as response:
                html = await response.text()
                compressed_html = gzip.compress(html.encode("utf-8"))
                with open(os.path.join(path, file_name + ".html.gz"), "wb") as file:
                    file.write(compressed_html)
