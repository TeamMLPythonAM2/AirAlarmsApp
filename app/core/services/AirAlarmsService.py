from pydantic import BaseModel
from shared.ABRequestService import ABRequestService
from dotenv import load_dotenv
import requests, os, json

load_dotenv()

ALARMS_API_KEY = os.getenv("ALARMS_API_KEY")
AIR_URL = 'https://api.alerts.in.ua//v1/iot/active_air_raid_alerts_by_oblast.json'


def get_obl_names():
    with open("oblasts.json", "r", encoding="utf-8") as f:
        return json.load(f).get("oblasts", [])


class AirAlarmOblast(BaseModel):
    oblast_statuses: list[dict[str, str]]


class AirAlarmsService(ABRequestService[AirAlarmOblast]):

    @staticmethod
    def request() -> AirAlarmOblast:
        params = {
            "token": ALARMS_API_KEY,
        }

        oblasts = get_obl_names()

        response = requests.get(AIR_URL, params=params)
        data = response.json()
        print(data)

        statuses = {
            "A": "active",
            "N": "no_alert",
            "P": "partial"
        }

        oblast_statuses = [
            {"location_title": oblasts[i], "status": statuses.get(data[i])}
            for i in range(len(data))
        ]

        print(oblast_statuses)
        return AirAlarmOblast(**{"oblast_statuses": oblast_statuses})


AirAlarmsService.request()
