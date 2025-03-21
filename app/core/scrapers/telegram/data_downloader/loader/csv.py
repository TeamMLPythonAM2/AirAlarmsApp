import datetime as dt
import logging
from pathlib import Path
from typing import get_type_hints

import pandas as pd

from ..dict_types.message import MessageAttributes

logger = logging.getLogger(__name__)


class CSVMessageWriter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_messages(
        self, messages: list[MessageAttributes],
        min_date: dt.datetime, max_date: dt.datetime
    ) -> None:
        """
        Write messages for a dialog to a CSV file.
        """
        if messages:
            df = pd.DataFrame(messages)
        else:
            columns = list(get_type_hints(MessageAttributes).keys())
            df = pd.DataFrame(columns=columns)
        filename = f"{min_date.strftime('%Y-%m-%d_%H')}-{max_date.strftime('%Y-%m-%d_%H')}.csv"
        write_path = self.output_dir / filename
        df.to_csv(write_path, index=False, encoding="utf-8-sig")
        # logger.debug("saved messages for %d to %s", dialog["id"], write_path)
