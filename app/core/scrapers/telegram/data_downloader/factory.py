import logging
import telethon
from app.config import Config

from app.core.scrapers.telegram.data_downloader import settings
from app.core.scrapers.telegram.data_downloader.dict_types.date import DateRange
from app.core.scrapers.telegram.data_downloader.loader.csv import CSVMessageWriter
from app.core.scrapers.telegram.data_downloader.processor.dialog_retriever import DialogRetriever
from app.core.scrapers.telegram.data_downloader.processor.message_downloader import MessageDownloader

logger = logging.getLogger(__name__)


async def create_telegram_client(session_name: str) -> telethon.TelegramClient:
    logger.debug("creating telegram client...")
    client = telethon.TelegramClient(
        session_name,
        Config.API_ID,
        Config.API_HASH,
        system_version=settings.CLIENT_SYSTEM_VERSION,
    )

    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(Config.API_PHONE)
        await client.sign_in(Config.API_PHONE, input('Enter code from telegram: '))

    return client

async def create_csv_message_saver() -> CSVMessageWriter:
    return CSVMessageWriter(settings.DATA_FOLDER)

async def create_dialog_retriever(
    telegram_client: telethon.TelegramClient,
) -> DialogRetriever:
    logger.debug("creating dialog downloader...")
    return DialogRetriever(telegram_client)

async def create_message_downloader(
    telegram_client: telethon.TelegramClient,
    date_range: DateRange,
) -> MessageDownloader:
    logger.debug("creating message downloader...")
    downloader = MessageDownloader(
        telegram_client,
        await create_csv_message_saver(),
        date_range
    )
    downloader.concurrent_dialog_downloads = settings.CONCURRENT_DIALOG_DOWNLOADS
    return downloader
