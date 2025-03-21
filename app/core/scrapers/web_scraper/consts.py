from pydantic import StringConstraints
from typing import Annotated

URL_PATTERN = Annotated[str, StringConstraints(pattern=r"https?://[-.a-zA-Z]{1,}")]
ENDPOINT_PATTERN = Annotated[str, StringConstraints(pattern=r"(/[a-zA-Z.-&?\d]{1,}){1,6}")]
