import asyncio
import logging
import typing
from app.core.scrapers.telegram.config import Config

import telethon
from telethon.tl import custom as tl_custom
from telethon.tl import types as tl_types

from ..dict_types.dialog import DialogMemberData, DialogMetadata, DialogType

logger = logging.getLogger(__name__)


class DialogWriter(typing.Protocol):
    def write_dialog(self, data: DialogMetadata) -> None: ...


class DialogDownloader:
    """
    Class for downloading and saving metadata of all user's dialogs.

    Attributes:
        telegram_client (telethon.TelegramClient): Telegram client for fetching the dialogs
        dialog_writer (DialogWriter): Dialog writer for saving the dialogs
    """

    def __init__(
        self,
        telegram_client: telethon.TelegramClient,
        dialog_writer: DialogWriter,
    ):
        self.dialog_writer = dialog_writer
        self.client = telegram_client

    async def get_dialogs(self) -> list[DialogMemberData]:
        """
        Returns:
            list[DialogMemberData]: KALL if the save was successful
        """
        logger.debug("retrieving dialog list...")
        dialogs: list[tl_custom.Dialog] = await self.client.get_dialogs()
        logger.info("found %d dialogs", len(dialogs))

        tasks = []
        # * process each dialog asynchronously, therefore increasing throughput
        for dialog in dialogs:
            if dialog.id not in Config.CHANNEL_IDS_LIST:
                continue
            task = asyncio.create_task(self._save_dialog(dialog))
            tasks.append(task)

        # logger.debug("gathering dialog saving tasks...")
        dialogs_metadata = await asyncio.gather(*tasks)
        # print(dialogs_info)

        # logger.info("dialogs list saved successfully")
        return dialogs_metadata

    @staticmethod
    async def _save_dialog(dialog: tl_custom.Dialog):
        dialog_id = dialog.id
        dialog_name = dialog.name
        # dialog_members: list[DialogMemberData] = []

        logger.info("dialog #%d: starting processing...", dialog_id)

        type_to_enum = {
            dialog.is_user: DialogType.PRIVATE,
            dialog.is_group: DialogType.GROUP,
            dialog.is_channel: DialogType.CHANNEL,
        }
        dialog_type = type_to_enum.get(True, DialogType.UNKNOWN)

        # logger.debug("dialog #%d: getting participants...", dialog_id)
        # try:
        #     users: list[tl_types.User] = await self.client.get_participants(dialog)
        # except telethon.errors.ChatAdminRequiredError as e:
        #     logger.error(
        #         "dialog #%d: getting participants: admin required: %s", dialog_id, e
        #     )
        # except telethon.errors.ChannelPrivateError as e:
        #     logger.error(
        #         "dialog #%d: getting participants: channel private: %s", dialog_id, e
        #     )
        # except telethon.errors.ChannelInvalidError as e:
        #     logger.error(
        #         "dialog #%d: getting participants: channel invalid: %s", dialog_id, e
        #     )
        # except telethon.errors.RPCError as e:
        #     logger.error(
        #         "dialog #%d: getting participants: unknown error: %s", dialog_id, e
        #     )
        # else:
        #     logger.debug("dialog #%d: processing participants...", dialog_id)
        #     dialog_members = [
        #         DialogMemberData(
        #             user_id=user.id,
        #             first_name=user.first_name,
        #             last_name=user.last_name,
        #             username=user.username,
        #             phone=user.phone,
        #         )
        #         for user in users
        #         if user.username is not None
        #     ]  # * list comprehension is generally faster than for loop

        return DialogMetadata(
            id=dialog_id,
            name=dialog_name,
            type=dialog_type,
            # users=dialog_members,
        )

        # self.dialog_writer.write_dialog(
        #     DialogMetadata(
        #         id=dialog_id,
        #         name=dialog_name,
        #         type=dialog_type,
        #         # users=dialog_members,
        #     )
        # )
        #
        # logger.info("dialog #%d: successfully saved", dialog_id)
