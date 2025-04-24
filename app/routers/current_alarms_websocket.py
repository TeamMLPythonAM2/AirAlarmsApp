from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import asyncio
from app.core.services.AirAlarmsService import AirAlarmsService
from app.city_convertion_dict import city_dict

router_ws = APIRouter()


@router_ws.websocket('/ws/current_alerts')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Connected")
    try:
        while True:
            alert_info = await AirAlarmsService.request_current(all_oblasts=True)
            clean_data = list(map(lambda x: {**x, "oblast": city_dict.get(x["oblast"])}, alert_info))
            the_cleanest_list_ever = [x["oblast"] for x in clean_data if x.get("alert") == "AIR"]
            await websocket.send_json(the_cleanest_list_ever)
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        print("Disconnected")
# returns list with oblasts with alarms
