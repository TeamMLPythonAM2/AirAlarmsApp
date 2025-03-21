from pydantic import StringConstraints
from typing import Annotated
from pathlib import Path
import os

URL_PATTERN = Annotated[str, StringConstraints(pattern=r"https?://[-.a-zA-Z]{1,}")]
ENDPOINT_PATTERN = Annotated[str, StringConstraints(pattern=r"(/[a-zA-Z.-&?\d]{1,}){1,6}")]
FILES_PATH = os.path.join(Path(__file__).resolve().parents[4], "files")
FIND_TAG = "Russian Offensive Campaign Assessment"


