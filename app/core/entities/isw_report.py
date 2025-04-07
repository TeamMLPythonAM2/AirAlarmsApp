from pydantic import BaseModel
from app.config.utils import *
from typing import Optional

class ISWReport(BaseModel):
    date: str
    short_url: Optional[str]
    full_url: Optional[str]
    text_data: str
    html_data: str
    text_lemm: str
    text_stemm: str

    def __init__(self, date, html_data, short_url = None):
        if short_url:
            full_url = Config.ISW_URL + short_url
        else:
            full_url = None
        text_data = extract_text_from_html(html_data)
        tokens = tokenize(text_data)
        super().__init__(
            date=date,
            short_url=short_url,
            full_url=full_url,
            text_data=text_data,
            html_data=html_data,
            text_lemm=lemmatize(tokens),
            text_stemm=stem(tokens),
        )

