from fastapi import HTTPException
from pydantic import BaseModel
from app.core.services.shared.ABRequestService import ABRequestService
import aiohttp
from app.config.configuration import Config

class AirAlarmRegions(BaseModel):
    oblast: str
    alert: str


class AirAlarmsService(ABRequestService[AirAlarmRegions]):
    HEADERS = {
        "Authorization": Config.ALARMS_API_KEY
    }

    @classmethod
    async def get_response(cls, url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url, headers=AirAlarmsService.HEADERS) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise HTTPException(status_code=500, detail=f"Error: {response.status} - {response.reason}")

    @staticmethod
    async def get_all_regions():
        """
        return a list of all oblasts and cities stored as states
        """
        data = await AirAlarmsService.get_response(Config.LIST_OF_REGIONS_URL)

        oblasts = []
        for info in data["states"]:
            region_type = info["regionType"]
            region_name = info["regionName"]
            if region_type == "State" and region_name not in Config.EXCLUDED_REGIONS:
                oblasts.append(region_name)
        return oblasts

    @staticmethod
    async def request_current(all_oblasts: bool = False):
        """
        return either the regions with active alerts or all regions
        """
        data = await AirAlarmsService.get_response(Config.AIR_URL)

        oblast_statuses = []
        for info in data:
            region_type = info["regionType"]
            region_name = info["regionName"]
            active_alerts = info.get("activeAlerts")

            if region_type == "State" and region_name not in Config.EXCLUDED_REGIONS:
                alerts = active_alerts[0].get("type")
                oblast_statuses.append(AirAlarmRegions(oblast=region_name, alert=alerts).model_dump())

        if all_oblasts:
            list_of_regions = await AirAlarmsService.get_all_regions()
            for region in list_of_regions:
                if not any(info["oblast"] == region for info in oblast_statuses):
                    oblast_statuses.append(AirAlarmRegions(oblast=region, alert="NO_ALERT").model_dump())

        return oblast_statuses
