from fastapi import FastAPI, Request, Response
# from logs.logger import loggable, logger
from app.routers.current_alarms_websocket import router_ws
from app.routers.current_predict_endpoint import router_get

app = FastAPI()

app.include_router(router_ws)
app.include_router(router_get)


# @app.get("/")
# @loggable
# async def root(request: Request, response: Response):
#     return {"content": {"Hello": "World"}, "status_code": 200}
