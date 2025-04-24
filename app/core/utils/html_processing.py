import gzip
import re
import os
import pandas as pd
from pathlib import Path
import datetime as dt

from app.config.configuration import Config
from app.core.entities.isw_report import ISWReport


def load_latest_html_file(year: str):
    path = Path(os.path.join(Config.FULL_REPORTS_PATH, year))
    files = [f for f in path.iterdir() if f.is_file() and f.name.endswith(".gz")]

    pattern = re.compile(r"([a-zA-Z]+)_(\d+)\.html\.gz")
    months = {name.lower(): idx for idx, name in enumerate(
        pd.date_range("2024-01-01", "2024-12-31", freq="MS").strftime('%B'), 1
    )}

    dated_files = []
    for file in files:
        match = pattern.match(file.name)
        if match:
            month_str, day_str = match.groups()
            month_num = months.get(month_str.lower())
            if month_num:
                try:
                    file_date = dt.datetime(int(year), month_num, int(day_str))
                    dated_files.append((file_date, file))
                except ValueError:
                    continue

    if not dated_files:
        raise FileNotFoundError(f"Could not find any valid file for {year}")

    latest_date, latest_file = max(dated_files, key=lambda x: x[0])

    file_content = read_gzip_file(latest_file)
    report = ISWReport(
        date=str(latest_date.date()),
        html_data=file_content
    )
    return pd.DataFrame([report.model_dump()])


def read_gzip_file(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return f.read()
