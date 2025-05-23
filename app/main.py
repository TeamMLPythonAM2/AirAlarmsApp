from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# from logs.logger import loggable, logger
from app.routers.current_alarms_websocket import router_ws
from app.routers.current_predict_endpoint import router_get
from app.routers.predict_for_all_hours_endpoint import router_alarms_all
from app.routers.update_predictions import router_predict


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="ui/dist", html=True), name="static")

app.include_router(router_ws, prefix="/api")
app.include_router(router_get, prefix="/api")
app.include_router(router_alarms_all, prefix="/api")
app.include_router(router_predict, prefix="/api")


@app.get("/{full_path:path}")
async def root(full_path: str):
    return FileResponse("ui/dist/index.html")
