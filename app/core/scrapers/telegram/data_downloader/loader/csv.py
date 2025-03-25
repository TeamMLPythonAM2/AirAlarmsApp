import logging
from pathlib import Path
from typing import get_type_hints
import pandas as pd

from app.core.scrapers.telegram.data_downloader.dict_types.message import MessageAttributes
from app.core.scrapers.telegram.data_downloader.dict_types.date import DateRange

logger = logging.getLogger(__name__)


class CSVMessageWriter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def write_messages(
        self, messages: list[MessageAttributes],
        date_range: DateRange
    ) -> None:
        """
        Write messages to a CSV file.
        """
        if messages:
            df = pd.DataFrame(messages)
        else:
            columns = list(get_type_hints(MessageAttributes).keys())
            df = pd.DataFrame(columns=columns)
        filename = (f"{date_range['min_d'].strftime('%Y-%m-%d_%H')}"
                    f"-{date_range['max_d'].strftime('%Y-%m-%d_%H')}.csv")
        write_path = self.output_dir / filename
        df.to_csv(write_path, index=False, encoding="utf-8-sig")
        logger.debug("saved messages to %s", write_path)
