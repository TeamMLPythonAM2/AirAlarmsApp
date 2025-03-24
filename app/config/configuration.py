import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Annotated

from pydantic import StringConstraints

load_dotenv()


class Config:
    TEST_SECRET = os.environ.get("TEST_SECRET")
    SHORT_REPORTS_PATH = os.path.join(Path(__file__).resolve().parents[2], "files", "isw_reports", "short_reports")
    FULL_REPORTS_PATH = os.path.join(Path(__file__).resolve().parents[2], "files/isw_reports/full_reports")
    LINKS_PATH = os.path.join(Path(__file__).resolve().parents[2], "files/isw_reports/links")
    URL_PATTERN = Annotated[str, StringConstraints(pattern=r"https?://[-.a-zA-Z]{1,}")]
