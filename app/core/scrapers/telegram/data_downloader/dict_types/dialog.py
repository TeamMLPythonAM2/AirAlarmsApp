from enum import Enum
from typing import TypedDict


class DialogType(Enum):
    PRIVATE = "private"
    GROUP = "group"
    CHANNEL = "channel"
    UNKNOWN = "unknown"

class DialogMetadata(TypedDict):
    id: int
    name: str
    type: DialogType
