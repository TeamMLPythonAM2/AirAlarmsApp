from pathlib import Path
import os, pandas as pd
from app.config.configuration import Config
from app.config.utils import read_gzip_file
from app.core.entities.isw_report import ISWReport

def load_html_files_to_parquet(year: str):
    path = Path(os.path.join(Config.FULL_REPORTS_PATH, year))
    cont = []
    for directory in path.iterdir():
        if str(directory.name).find(".gz") == -1:
            continue
        date = directory.name.split(".")[0].split("_")
        date.insert(0, path.name)
        date = '_'.join(date)
        date = str(pd.to_datetime(date, format="%Y_%B_%d"))

        file = read_gzip_file(directory)
        report = ISWReport(
            date=date,
            html_data=file
        )
        cont.append(report.model_dump())
    df_main = pd.read_parquet(Config.ISW_PARQUET_PATH)
    df = pd.DataFrame(cont)
    df_main = pd.concat([df_main, df], ignore_index=True)
    df_main.to_parquet(Config.ISW_PARQUET_PATH)