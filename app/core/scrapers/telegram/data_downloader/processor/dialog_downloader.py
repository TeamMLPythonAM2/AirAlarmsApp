import asyncio
import logging
from app.core.scrapers.telegram.config import Config

import telethon
from telethon.tl import custom as tl_custom
from telethon.tl import types as tl_types

from ..dict_types.dialog import DialogMemberData, DialogMetadata, DialogType

logger = logging.getLogger(__name__)


class DialogDownloader:
    """
    Class for downloading and saving metadata of all user's dialogs.

    Attributes:
        telegram_client (telethon.TelegramClient): Telegram client for fetching the dialogs
    """

    def __init__(self, telegram_client: telethon.TelegramClient):
        self.client = telegram_client

    async def get_dialogs(self) -> list[DialogMetadata]:
        """
        Returns:
            KALL list]: if the save was successful
        """
        logger.debug("retrieving dialog list...")
        dialogs: list[tl_custom.Dialog] = await self.client.get_dialogs()
        logger.info("found %d dialogs", len(dialogs))

        tasks = []
        # * process each dialog asynchronously, therefore increasing throughput
        for dialog in dialogs:
            # print(f'{dialog.name} : {dialog.id}')
            if dialog.id not in Config.CHANNEL_IDS_LIST:
                continue
            task = asyncio.create_task(self._save_dialog(dialog))
            tasks.append(task)

        # logger.debug("gathering dialog saving tasks...")
        dialogs_metadata = await asyncio.gather(*tasks)
        # logger.info("dialogs list saved successfully")
        return dialogs_metadata

    @staticmethod
    async def _save_dialog(dialog: tl_custom.Dialog):
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
