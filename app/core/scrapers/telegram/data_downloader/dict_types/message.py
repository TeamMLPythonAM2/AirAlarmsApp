import datetime as dt
from enum import Enum
from typing import Optional, TypedDict


class MessageType(Enum):
    TEXT = "text"
    STICKER = "sticker"
    VIDEO = "video"
    VOICE = "voice"
    PHOTO = "photo"

class MessageAttributes(TypedDict):
    channel_id: int
    id: int
    date: Optional[dt.datetime]
    content: str
