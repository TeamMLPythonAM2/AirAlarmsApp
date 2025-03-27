import datetime as dt
from typing import Optional, TypedDict


class MessageAttributes(TypedDict):
    channel_id: int
    id: int
    date: Optional[dt.datetime]
    content: str
