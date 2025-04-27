from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# from logs.logger import loggable, logger
from app.routers.current_alarms_websocket import router_ws
from app.routers.current_predict_endpoint import router_get
from app.routers.predict_for_all_hours_endpoint import router_task_7
from app.routers.update_predictions import router_predict


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory="dist", html=True), name="static")
app.include_router(router_ws)
app.include_router(router_get)
app.include_router(router_task_7)
app.include_router(router_predict)