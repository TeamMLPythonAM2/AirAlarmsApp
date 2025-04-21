from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

# from logs.logger import loggable, logger
from app.routers.current_alarms_websocket import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(router)


@app.get("/")
# @loggable
async def root(request: Request, response: Response):
    return {"content": {"Hello": "World"}, "status_code": 200}
