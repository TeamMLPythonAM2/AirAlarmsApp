import os
from pathlib import Path
from typing import Annotated

from pydantic import StringConstraints

URL_PATTERN = Annotated[str, StringConstraints(pattern=r"https?://[-.a-zA-Z]{1,}")]
ENDPOINT_PATTERN = Annotated[
    str, StringConstraints(pattern=r"(/[a-zA-Z.-&?\d]{1,}){1,6}")
]
FILES_PATH = os.path.join(Path(__file__).resolve().parents[4], "files")
