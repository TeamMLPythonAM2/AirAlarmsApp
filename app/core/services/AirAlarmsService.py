from pydantic import BaseModel
from shared.ABRequestService import ABRequestService
import aiohttp, asyncio
from app.config.configuration import Config

ALARMS_API_KEY = Config.ALARMS_API_KEY
LIST_OF_REGIONS_URL = Config.LIST_OF_REGIONS_URL
AIR_URL = Config.AIR_URL

EXCLUDED_REGIONS = Config.EXCLUDED_REGIONS


class AirAlarmRegions(BaseModel):
    oblast: str
    alert: str


class AirAlarmsService(ABRequestService[AirAlarmRegions]):
    headers = {
        "Authorization": ALARMS_API_KEY
    }

    @staticmethod
    async def get_all_regions():
        """
        return a list of all oblasts and cities stored as states
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(LIST_OF_REGIONS_URL, headers=AirAlarmsService.headers) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    print(f"Error: {response.status} - {response.reason}")

        oblasts = []
        for info in data["states"]:
            region_type = info["regionType"]
            region_name = info["regionName"]
            if region_type == "State" and region_name not in EXCLUDED_REGIONS:
                oblasts.append(region_name)
        return oblasts

    @staticmethod
    async def request_current(all_oblasts: bool = False):
        """
        return either the regions with active alerts or all regions
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(AIR_URL, headers=AirAlarmsService.headers) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    print(f"Error: {response.status} - {response.reason}")

        # print(data)

        oblast_statuses = []
        for info in data:
            region_type = info["regionType"]
            region_name = info["regionName"]
            active_alerts = info.get("activeAlerts")

            if region_type == "State" and region_name not in EXCLUDED_REGIONS:
                alerts = active_alerts[0].get("type")
                oblast_statuses.append(AirAlarmRegions(oblast=region_name, alert=alerts).model_dump())

        if all_oblasts:
            list_of_regions = await AirAlarmsService.get_all_regions()
            # print(list_of_regions)
            for region in list_of_regions:
                if not any(info["oblast"] == region for info in oblast_statuses):
                    oblast_statuses.append(AirAlarmRegions(oblast=region, alert="NO_ALERT").model_dump())

        print(oblast_statuses)
        return oblast_statuses


async def main():
    await AirAlarmsService.request_current(all_oblasts=False)


asyncio.run(main())
