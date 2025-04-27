import aiohttp
from fastapi import HTTPException
from pydantic import validate_call

from app.config.configuration import Config
from datetime import datetime

from app.core.entities.isw_report import ISWReport


class ISWScraper:
    START = datetime.fromisocalendar(2022, 8, 4)

    @staticmethod
    @validate_call
    async def get_page_content(
            full_url: Config.URL_PATTERN
    ):
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.get(full_url) as response:
                if response.status != 200:
                    return
                html = await response.text(encoding="utf-8")
                return html

    @classmethod
    async def get_full_page_content(cls, dtt: datetime):
        if cls.START > dtt:
            raise HTTPException(status_code=500, detail="Too early date")
        for endpoint in [
            dtt.strftime("UkrWar%m%d%y"),
            f"RusCampaign{dtt.strftime('%b')}{dtt.day}",
            dtt.strftime("UkrWar%m%d%Y")
        ]:
            if data := await ISWScraper.get_page_content(Config.ISW_URL + endpoint):
                return ISWReport(
                    date=dtt.strftime("%Y-%m-%d"),
                    html_data=data
                )
