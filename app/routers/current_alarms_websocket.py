from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import asyncio
from app.core.services.AirAlarmsService import AirAlarmsService

router = APIRouter()


@router.websocket('/ws/current_alerts')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Connected")
    try:
        while True:
            alert_info = await AirAlarmsService.request_current(all_oblasts=True)
            await websocket.send_json(alert_info)
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        print("Disconnected")
# returns json with city - no alert or alert every 30 sec
