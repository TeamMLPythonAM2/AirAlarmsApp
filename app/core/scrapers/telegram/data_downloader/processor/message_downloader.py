import asyncio
import typing
from itertools import chain
from app.logs.logger import logger
from app.core.scrapers.telegram import consts

import telethon
from telethon.tl import types as tl_types
from telethon.tl.custom.message import Message as TLMessage

from app.core.scrapers.telegram.data_downloader.dict_types.date import DateRange
from app.core.scrapers.telegram.data_downloader.dict_types.dialog import DialogMetadata
from app.core.scrapers.telegram.data_downloader.dict_types.message import MessageAttributes
from app.core.scrapers.telegram.data_downloader.loader.csv import CSVMessageWriter


class MessageDownloader:
    def __init__(
        self,
        client: telethon.TelegramClient,
        message_writer: CSVMessageWriter,
        date_range: DateRange,
    ) -> None:
        self.client = client
        self.message_writer = message_writer
        self._semaphore = asyncio.Semaphore(5)
        self.date_range = date_range

    @property
    def concurrent_dialog_downloads(self) -> int:
        """
        Current number of dialogs, that will be processed concurrently during download.
        """
        return self._semaphore._value  # pylint: disable=protected-access

    @concurrent_dialog_downloads.setter
    def concurrent_dialog_downloads(self, value: int) -> None:
        self._semaphore = asyncio.Semaphore(value)

    @staticmethod
    async def _reformat_message(message: TLMessage, channel_id: int) -> MessageAttributes:
        msg_attributes: MessageAttributes = {
            "channel_id": channel_id,
            "id": message.id,
            "date": message.date,
            "content": message.message or ""
        }
        return msg_attributes

    async def _get_message_iterator(self, dialog: DialogMetadata) -> typing.AsyncIterator[TLMessage]:
        logger.debug("dialog #%d: creating message iterator", dialog["id"])
        tg_entity = await self.client.get_entity(dialog["id"])

        if isinstance(tg_entity, list):
            tg_entity = tg_entity[0]
        async for message in self.client.iter_messages(
            tg_entity, wait_time=5, offset_date=self.date_range['max_d']
        ):
            if message.date < self.date_range['min_d']:
                break
            yield message

    async def _get_dialog_messages(self, dialog: DialogMetadata) -> list[MessageAttributes]:
        logger.info("dialog #%d: receiving messages...", dialog["id"])
        dialog_messages: list[MessageAttributes] = []
        msg_count = 0

        async for m in self._get_message_iterator(dialog):
            msg_count += 1
            if msg_count % 1000 == 0:
                logger.debug(
                    "dialog #%d: processing message number %d", dialog["id"], msg_count
                )

            if not await self._is_relevant_message(m.message or ''):
                continue

            dialog_messages.append(await self._reformat_message(m, dialog['id']))

        logger.info("dialog #%d: messages received", dialog["id"])
        return dialog_messages


    @staticmethod
    async def _is_relevant_message(message: str) -> bool:
        return any(word in message.lower() for word in consts.TARGET_WORDS)

    async def _semaphored_download_dialog(self, *args, **kwargs) -> list[MessageAttributes]:
        """
        A utility function to restrict throughput of `_download_dialog` method.
        It is necessary due to Telegram's request rate limits, which produces
        "429 Too Many Requests" errors.
        """
        async with self._semaphore:
            return await self._get_dialog_messages(*args, **kwargs)

    async def download_dialogs(self, dialogs: list[DialogMetadata]) -> None:
        """
        Provided a `dialogs` list, download messages from each dialog and save them.
        """
        logger.info("downloading messages from %d dialogs...", len(dialogs))
        tasks = []
        for dialog in dialogs:
            # TODO: up for debate: move semaphored download to a decorator
            tasks.append(self._semaphored_download_dialog(dialog))
        dialogs_messages = await asyncio.gather(*tasks)
        messages = list(chain.from_iterable(dialogs_messages))
        await self.message_writer.write_messages(messages, self.date_range)

        logger.info("all dialogs downloaded")
        return
