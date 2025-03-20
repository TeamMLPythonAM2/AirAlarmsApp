import logging
from fastapi import FastAPI, Request
import uvicorn
from logs.logger import loggable

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
@loggable
async def root(request: Request):
    return {"content": {"Hello": "World"}, "status_code": 200}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
