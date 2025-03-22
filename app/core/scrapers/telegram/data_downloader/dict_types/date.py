import datetime as dt
from typing import TypedDict


class DateRange(TypedDict):
    min_d: dt.datetime
    max_d: dt.datetime
