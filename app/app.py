from fastapi import FastAPI, Request, Response
from logs.logger import loggable, logger

app = FastAPI()


@app.get("/")
@loggable
async def root(request: Request, response: Response):
    return {"content": {"Hello": "World"}, "status_code": 200}
