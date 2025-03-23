import logging
from config.logger import loggable
from config import *
from fastapi import FastAPI, Request, Response, HTTPException
import uvicorn

logger = logging.getLogger("main")
app = FastAPI()


@app.get("/")
@loggable
async def root(request: Request, response: Response):
    return "<div>Hello</div>"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
