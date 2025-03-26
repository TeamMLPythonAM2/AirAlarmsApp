import logging
from fastapi import FastAPI, Request
from logs.logger import loggable

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
@loggable
async def root(request: Request):
    return {"content": {"Hello": "World"}, "status_code": 200}
