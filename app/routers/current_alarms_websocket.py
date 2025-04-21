from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import asyncio
from app.core.services.AirAlarmsService import AirAlarmsService
from app.city_convertion_dict import city_dict

router = APIRouter()


@router.websocket('/ws/current_alerts')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Connected")
    try:
        while True:
            alert_info = await AirAlarmsService.request_current(all_oblasts=True)
            clean_data = list(map(lambda x: {**x, "oblast": city_dict.get(x["oblast"])}, alert_info))
            await websocket.send_json(clean_data)
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        print("Disconnected")
# returns json with city - no alert or alert every 30 sec
