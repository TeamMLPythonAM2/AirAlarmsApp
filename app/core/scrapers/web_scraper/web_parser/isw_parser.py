import asyncio
import gzip
import json
import os

import regex as re
from fastapi import HTTPException

from app.config.configuration import Config
from app.core.scrapers.web_scraper.isw_enum import ISWEnum


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

    async def parse_href(self, file_name: str, path: str):
        with gzip.open(filename=os.path.join(path, file_name)) as file:
            file_str = file.read().decode()
            file.close()
            matches = re.finditer(self.HREF_PATTERN, file_str)
            self.matches_iter = matches
            self.href_json_name = file_name[:-8]

    async def find_write_href(self, path: str):
        if not self.matches_iter.captures():
            raise HTTPException(500, "No matches for isw parser")

        for row in self.matches_iter:
            href = re.search(self.URL_DATE_PATTERN, row.captures()[0])
            date = re.search(self.DATE_PATTERN, row.captures()[0])
            if href and date:
                self.href_json[date.captures()[0].replace(" ", "_").lower()] = (
                    href.captures()[0][1:-2]
                )
        with open(
                os.path.join(path, self.href_json_name + ".json"), "w"
        ) as json_file:
            json_file.write(json.dumps(self.href_json))
            json_file.close()
