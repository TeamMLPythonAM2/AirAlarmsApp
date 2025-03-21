import datetime as dt
import asyncio

from data_downloader.factory import (
    create_dialog_downloader,
    create_telegram_client,
)

# from typing import Callable
import telethon

from data_downloader import settings
from app.core.scrapers.telegram.exceptions import (
    UninitializedTakeoutSessionException,
    InvalidDateRangeException
)
# from data_downloader.dict_types.dialog import DialogMetadata, DialogType
from data_downloader.factory import (
    create_json_dialog_reader_writer,
    create_message_downloader
)

class TelegramScraper:
    @classmethod
    async def scrape(cls, date: dt.datetime, end_date: dt.datetime = None): # -> list[TelegramDTO]:
        if end_date is None:
            max_date = date.replace(minute=0, second=0, microsecond=0)
            min_date = max_date - dt.timedelta(hours=1)
        else:
            max_date = end_date.replace(minute=0, second=0, microsecond=0)
            min_date = date.replace(minute=0, second=0, microsecond=0)

        if max_date <= min_date:
            raise InvalidDateRangeException("Maximum date must be later than the minimum date.")

        print(f'min_date: {min_date}')
        print(f'max_date: {max_date}')

        client = await create_telegram_client('session')
        dialog_downloader = create_dialog_downloader(client)

        async with client:
            dialogs = await dialog_downloader.get_dialogs()
        # return
        # dialog_reader = create_json_dialog_reader_writer()
        # dialogs = dialog_reader.read_all_dialogs()

        # client = create_telegram_client('session')
        # print("downloading dialogs...")
        async with client:
            try:
                async with client.takeout(
                    finalize=settings.CLIENT_TAKEOUT_FINALIZE,
                    contacts=settings.CLIENT_TAKEOUT_FETCH_CONTACTS,
                    users=settings.CLIENT_TAKEOUT_FETCH_USERS,
                    chats=settings.CLIENT_TAKEOUT_FETCH_GROUPS,
                    megagroups=settings.CLIENT_TAKEOUT_FETCH_MEGAGROUPS,
                    channels=settings.CLIENT_TAKEOUT_FETCH_CHANNELS,
                    files=settings.CLIENT_TAKEOUT_FETCH_FILES,
                ) as takeout:
                    message_downloader = create_message_downloader(takeout, min_date, max_date)
                    await message_downloader.download_dialogs(dialogs)
            except telethon.errors.TakeoutInitDelayError as e:
                raise UninitializedTakeoutSessionException(
                    "\nWhen initiating a `takeout` session, Telegram requires a cooling period "
                    "between data exports.\n"
                    f"Initial message: {e}\n"
                    "Workaround: You can allow takeout by:\n"
                    "1. Opening Telegram service notifications (where you retrieved the login code)\n"
                    '2. Click allow on "Data export request"\n'
                ) from e
        print("dialogs downloaded")


        # return TelegramDTO(**{"prp": "", "ppp": ""})

if __name__ == '__main__':
    date = dt.datetime.now(dt.timezone.utc)
    asyncio.run(TelegramScraper.scrape(date))
