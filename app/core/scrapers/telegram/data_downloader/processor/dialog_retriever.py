import asyncio
import logging
from app.core.scrapers.telegram import consts

import telethon
from telethon.tl import custom as tl_custom
from telethon.tl import types as tl_types

from ..dict_types.dialog import DialogMetadata, DialogType

logger = logging.getLogger(__name__)


class DialogRetriever:
    def __init__(self, telegram_client: telethon.TelegramClient):
        self.client = telegram_client

    async def retrieve_dialogs(self) -> list[DialogMetadata]:
        logger.debug("retrieving dialog list...")
        dialogs: list[tl_custom.Dialog] = await self.client.get_dialogs()
        logger.info("found %d dialogs", len(dialogs))

        tasks = []
        # * process each dialog asynchronously, therefore increasing throughput
        for dialog in dialogs:
            if dialog.id not in consts.CHANNEL_IDS_LIST:
                continue
            task = asyncio.create_task(self._dialog_metadata(dialog))
            tasks.append(task)

        logger.debug("gathering dialog metadata tasks...")
        dialogs_metadata = await asyncio.gather(*tasks)
        logger.info("list of dialogs metadata retrieved successfully")
        return dialogs_metadata

    @staticmethod
    async def _dialog_metadata(dialog: tl_custom.Dialog) -> DialogMetadata:
        dialog_id = dialog.id
        dialog_name = dialog.name

        logger.info("dialog #%d: starting processing...", dialog_id)

        type_to_enum = {
            dialog.is_user: DialogType.PRIVATE,
            dialog.is_group: DialogType.GROUP,
            dialog.is_channel: DialogType.CHANNEL,
        }
        dialog_type = type_to_enum.get(True, DialogType.UNKNOWN)

        return DialogMetadata(
            id=dialog_id,
            name=dialog_name,
            type=dialog_type
        )
