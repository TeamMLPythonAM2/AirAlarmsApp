import gzip
import json
import os

import regex as re
from fastapi import HTTPException


class ISWLinksParser:
    HREF_PATTERN = re.compile(
        r"<a href=\"https?://.{1,30}\".{1,}((Click here to read|Ukraine Invasion Update)"
        r"(.{1,}\n){1,2}.{1,50}<strong>[A-Za-z]{1,10} \d{1,2}|"
        r"Russian Offensive Campaign Assessment, ?[A-Z][a-z]{1,10} ?\d{1,2})"
    )

    URL_DATE_PATTERN = re.compile(r"\"https?://.{1,30}\"[>\s]")
    DATE_PATTERN = re.compile(r"[A-Z][a-z]{1,10} \d{1,2}")

    def __init__(self):
        self.matches_iter = None
        self.href_json_name = None
        self.href_json: dict[str, str] = {}

    async def parse_href(self, file_name: str, path: str):
        with gzip.open(filename=os.path.join(path, file_name + ".html.gz")) as file:
            file_str = file.read().decode()
            file.close()
            self.matches_iter = re.finditer(self.HREF_PATTERN, file_str)
            self.href_json_name = file_name

    async def upload_from_hrefs(self, path: str):
        if not self.matches_iter:
            raise HTTPException(500, "No matches for isw parser")

        for row in self.matches_iter:
            href = re.search(self.URL_DATE_PATTERN, row.captures()[0])
            date = re.search(self.DATE_PATTERN, row.captures()[0])
            if href and date:
                self.href_json[date.captures()[0].replace(" ", "_").lower()] = (
                    href.captures()[0][1:-2]
                )
        with open(os.path.join(path, self.href_json_name + ".json"), "w") as json_file:
            json_file.write(json.dumps(self.href_json))
            json_file.close()
