import asyncio
import logging
import typing
from itertools import chain
from app.core.scrapers.telegram.config import Config

import telethon
from telethon.tl import types as tl_types
from telethon.tl.custom.message import Message as TLMessage

from .. import settings
from ..dict_types.dialog import DialogMetadata
from ..dict_types.message import MessageAttributes, MessageType, PeerID
from ..utils import async_retry
from ..loader.csv import CSVMessageWriter

logger = logging.getLogger(__name__)


class MessageDownloader:
    """
    Class for downloading and saving messages from user's dialogs.

    For detailed info on message data structure, see `MessageAttributes` class.

    Attributes:
        client (telethon.TelegramClient): Telegram client for fetching the messages
        message_writer (MessageWriter): Message writer for saving the messages
        reactions_limit_per_message (int): maximum amount of reactions to fetch per message
    """

    def __init__(
        self,
        client: telethon.TelegramClient,
        message_writer: CSVMessageWriter,
        *,
        reactions_limit_per_message: int,
    ) -> None:
        self.client = client
        self.message_writer = message_writer
        self.reactions_limit_per_message = reactions_limit_per_message
        self._semaphore = asyncio.Semaphore(5)
        self.min_date = None
        self.max_date = None

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
    def _reformat_message(message: TLMessage, channel_id: int) -> MessageAttributes:
        """
        Reformat a single message to a more convenient data structure.
        """
        msg_attributes: MessageAttributes = {
            "channel_id": channel_id,
            "id": message.id,
            "date": message.date,
            "message": message.message or ""
        }

        return msg_attributes

    @async_retry(
        telethon.errors.common.InvalidBufferError,
        base_sleep_time=settings.MESSAGE_REACTION_EXPONENTIAL_BACKOFF_SLEEP_TIME,
        max_tries=settings.MESSAGE_REACTION_EXPONENTIAL_BACKOFF_MAX_TRIES,
    )
    async def _get_message_reactions(
        self, message: TLMessage, dialog_peer: tl_types.TypeInputPeer
    ) -> dict[PeerID, tl_types.ReactionEmoji]:
        """
        Get reactions for a single message.

        Args:
            message (TLMessage): message to get reactions for
            dialog_peer (tl_types.TypeInputPeer): dialog to get the reactions from
                This is required because message id is relative to the dialog.

        Returns:
            dict[PeerID, tl_types.ReactionEmoji]
        """
        try:
            result: tl_types.messages.MessageReactionsList = await self.client(
                telethon.functions.messages.GetMessageReactionsListRequest(
                    peer=dialog_peer,
                    id=message.id,
                    limit=self.reactions_limit_per_message,
                )
            )  # type: ignore
        except telethon.errors.BroadcastForbiddenError:
            logger.debug("channel is broadcast: cannot retrieve reactions from message")
            reactions = {}
        except telethon.errors.MsgIdInvalidError:
            logger.debug("message %d not found", message.id)
            reactions = {}
        else:
            reaction_objects = result.reactions
            reactions = {
                PeerID(
                    telethon.utils.get_peer_id(reaction_object.peer_id)
                ): reaction_object.reaction
                for reaction_object in reaction_objects
                if isinstance(reaction_object.reaction, tl_types.ReactionEmoji)
            }

        return reactions

    async def _get_message_iterator(self, dialog: DialogMetadata) -> typing.AsyncIterator[TLMessage]:
        """
        Utility function to get an async iterator of messages from a dialog.
        We can't use plain `TelegramClient.iter_messages` method, because there can be caveats.
        """

        logger.debug("dialog #%d: creating message iterator", dialog["id"])
        # try:
        tg_entity = await self.client.get_entity(dialog["id"])
        # except ValueError as e:
        #     logger.error("dialog #%d: %s", dialog["id"], e)
        #     logger.info("init dialog %d through member username", dialog["id"])
        #
        #     username = None
        #     try:
        #         # dialog_metadata = self.dialog_reader.read_dialog(dialog["id"])
        #     except FileNotFoundError:
        #         logger.error("dialog #%d: not found", dialog["id"])
        #         raise
        #
        #     if (
        #         "users" in dialog_metadata
        #         and len(dialog_metadata["users"]) == 1
        #         and "username" in dialog_metadata["users"][0]
        #     ):
        #         username = dialog_metadata["users"][0]["username"]
        #     else:
        #         logger.error("dialog #%d: not a private chat", dialog["id"])
        #         return
        #
        #     if not username:
        #         # * user found, but username is empty
        #         logger.error(
        #             "dialog #%d: single user found, but username is empty", dialog["id"]
        #         )
        #         raise ValueError("username is empty") from e
        #
        #     tg_entity = await self.client.get_input_entity(username)
        # except Exception as e:  # pylint: disable=broad-except
        #     logger.error("dialog #%d: %s", dialog["id"], e)
        #     return

        if isinstance(tg_entity, list):
            tg_entity = tg_entity[0]
        async for message in self.client.iter_messages(
            tg_entity, wait_time=5, offset_date=self.max_date
        ):
            print(f'message.date - {message.date}')
            if message.date < self.min_date:
                break
            yield message

    async def _get_dialog_messages(self, dialog: DialogMetadata) -> list[MessageAttributes]:
        """
        Download messages from a single dialog and save them.
        """
        logger.info("dialog #%d: downloading messages...", dialog["id"])
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

            dialog_messages.append(self._reformat_message(m, dialog['id']))

        return dialog_messages
        # logger.info("dialog #%d: messages downloaded", dialog["id"])

    @staticmethod
    async def _is_relevant_message(message: str) -> bool:
        return any(word in message.lower() for word in Config.TARGET_WORDS)

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
        self.message_writer.write_messages(messages, self.min_date, self.max_date)

        logger.info("all dialogs downloaded")
        return
