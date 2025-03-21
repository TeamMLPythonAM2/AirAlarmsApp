import datetime as dt
import logging
import telethon
from app.config import Config

from . import settings
from .loader.json import JSONDialogReaderWriter
from .loader.csv import CSVMessageWriter
from .processor.dialog_downloader import DialogDownloader
from .processor.message_downloader import MessageDownloader

logger = logging.getLogger(__name__)


async def create_telegram_client(session_name: str) -> telethon.TelegramClient:
    logger.debug("creating telegram client...")
    client = telethon.TelegramClient(
        session_name,
        21838332, # Config.API_ID,
        '299ac999bca6df4b2f71a360a0f47fc3', # Config.API_HASH,
        system_version=settings.CLIENT_SYSTEM_VERSION,
    )

    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request("+380991037342") # Config.API_PHONE
        await client.sign_in("+380991037342", input('Enter code: '))

    return client

def create_json_dialog_reader_writer() -> JSONDialogReaderWriter:
    return JSONDialogReaderWriter(settings.DIALOGS_LIST_FOLDER)

def create_csv_message_saver() -> CSVMessageWriter:
    return CSVMessageWriter(settings.DIALOGS_DATA_FOLDER)

def create_dialog_downloader(
    telegram_client: telethon.TelegramClient,
) -> DialogDownloader:
    logger.debug("creating dialog downloader...")
    return DialogDownloader(telegram_client, create_json_dialog_reader_writer())

def create_message_downloader(
    telegram_client: telethon.TelegramClient,
    min_date: dt.datetime,
    max_date: dt.datetime,
) -> MessageDownloader:
    logger.debug("creating message downloader...")
    downloader = MessageDownloader(
        telegram_client,
        create_json_dialog_reader_writer(),
        create_csv_message_saver(),
        reactions_limit_per_message=settings.REACTIONS_LIMIT_PER_MESSAGE,
    )
    downloader.concurrent_dialog_downloads = settings.CONCURRENT_DIALOG_DOWNLOADS
    downloader.min_date = min_date.replace(tzinfo=dt.timezone.utc)
    downloader.max_date = max_date.replace(tzinfo=dt.timezone.utc)
    print(f'min_date: {downloader.min_date}')
    print(f'max_date: {downloader.max_date}')
    return downloader
