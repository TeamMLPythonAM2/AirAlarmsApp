from pydantic import BaseModel
from app.core.utils.isw import *


class ISWReport(BaseModel):
    date: str
    text_lemm: str

    def __init__(self, date, html_data):
        text_data = extract_text_from_html(html_data)
        tokens = tokenize(text_data)
        super().__init__(
            date=date,
            text_lemm=lemmatize(tokens),
        )
