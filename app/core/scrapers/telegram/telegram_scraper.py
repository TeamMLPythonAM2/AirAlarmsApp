import datetime as dt
import telethon

from app.core.scrapers.telegram.data_downloader.dict_types.date import DateRange
from app.core.scrapers.telegram.data_downloader.factory import (
    create_dialog_retriever,
    create_telegram_client,
    create_message_downloader
)
from app.core.scrapers.telegram.data_downloader import settings
from app.core.scrapers.telegram.data_downloader.dict_types.dialog import DialogMetadata
from app.core.scrapers.telegram.exceptions import (
    UninitializedTakeoutSessionException,
    InvalidDateRangeException
)


class TelegramScraper:
    @classmethod
    async def scrape_content(cls, target_date: dt.datetime, end_date: dt.datetime=None) -> None:
        date_range = cls._time_range(target_date, end_date)
        client = await create_telegram_client('session')
        dialogs = await cls._fetch_dialogs(client)

        await cls._download_messages(client, dialogs, date_range)

    @staticmethod
    def _time_range(target_date: dt.datetime, end_date: dt.datetime=None) -> DateRange:
        if end_date is None:
            max_date = target_date.replace(minute=0, second=0, microsecond=0)
            min_date = max_date - dt.timedelta(hours=1)
        else:
            max_date = end_date.replace(minute=0, second=0, microsecond=0)
            min_date = target_date.replace(minute=0, second=0, microsecond=0)

        if max_date <= min_date:
            raise InvalidDateRangeException("Maximum date must be later than the minimum date.")

        return DateRange(
            min_d=min_date.replace(tzinfo=dt.timezone.utc),
            max_d=max_date.replace(tzinfo=dt.timezone.utc)
        )

    @staticmethod
    async def _fetch_dialogs(client: telethon.TelegramClient) -> list[DialogMetadata]:
        async with client:
            dialog_downloader = await create_dialog_retriever(client)
            return await dialog_downloader.retrieve_dialogs()

    @classmethod
    async def _download_messages(
        cls,
        client: telethon.TelegramClient,
        dialogs: list[DialogMetadata],
        date_range: DateRange,
    ) -> None:
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
                    message_downloader = await create_message_downloader(takeout, date_range)
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
