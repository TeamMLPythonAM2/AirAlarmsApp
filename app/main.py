from fastapi import FastAPI
# from logs.logger import loggable, logger
from app.routers.current_alarms_websocket import router_ws
from app.routers.current_predict_endpoint import router_get
from app.routers.predict_for_all_hours_endpoint import router_task_7
from app.routers.update_predictions import router_predict

app = FastAPI()

app.include_router(router_ws)
app.include_router(router_get)
app.include_router(router_task_7)
app.include_router(router_predict)


# @app.get("/")
# @loggable
# async def root(request: Request, response: Response):
#     return {"content": {"Hello": "World"}, "status_code": 200}
