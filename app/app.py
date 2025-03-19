from logs.logger import loggable
from config import *
from fastapi import FastAPI, Request
import logging
import uvicorn

CONFIG = Config()
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
@loggable
async def root(request: Request):
    return {"Hello": "World", "status_code": 200}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
