import asyncio
import gzip
import json
import os
from typing import Optional

import regex as re

from app.core.scrapers.web_scraper.consts import FILES_PATH


class ISWParser:
    HREF_PATTERN = re.compile(
        r"<a href=\"https?://.{1,30}\".{1,}((Click here to read|Ukraine Invasion Update)(.{1,}\n){1,2}.{1,50}<strong>[A-Za-z]{1,10} \d{1,2}|"
        r"Russian Offensive Campaign Assessment, ?[A-Z][a-z]{1,10} ?\d{1,2})"
    )

    URL_DATE_PATTERN = re.compile(r"\"https?://.{1,30}\"[>\s]")
    DATE_PATTERN = re.compile(r"[A-Z][a-z]{1,10} \d{1,2}")

    def __init__(self):
        self.matches_iter = None
        self.href_json_name = None
        self.href_json: dict[str, str] = {}

    async def parse_href(self, file_name: str):
        with gzip.open(filename=os.path.join(FILES_PATH, file_name)) as file:
            file_str = file.read().decode()
            file.close()
            matches = re.finditer(self.HREF_PATTERN, file_str)
            self.matches_iter = matches
            self.href_json_name = file_name[:-8]

    async def find_write_href(self):
        if not self.matches_iter:
            raise ValueError("matches is empty")

        for row in self.matches_iter:
            href = re.search(self.URL_DATE_PATTERN, row.captures()[0])
            date = re.search(self.DATE_PATTERN, row.captures()[0])
            if href and date:
                self.href_json[date.captures()[0].replace(" ", "_").lower()] = (
                    href.captures()[0][1:-2]
                )
        with open(
            os.path.join(FILES_PATH, self.href_json_name + ".json"), "w"
        ) as json_file:
            json_file.write(json.dumps(self.href_json))
            json_file.close()


if __name__ == "__main__":
    par = ISWParser()
    asyncio.run(par.parse_href("REPORTS_2023.html.gz"))
    asyncio.run(par.find_write_href())
    print(par.matches_iter, par.href_json)
