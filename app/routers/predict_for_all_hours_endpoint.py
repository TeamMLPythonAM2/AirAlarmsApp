import pytz
from fastapi import APIRouter, Header
from datetime import datetime, timedelta
import pandas as pd
from app.config.configuration import Config
from app.utils.key_verification import key_check
import os

# Router just for task 7


# '%Y-%m-%d_%H'

current_time = datetime.now(tz=Config.KYIV_TZ).replace(minute=0, second=0, microsecond=0)
current_time = current_time.strftime("%Y-%m-%d_%H")

router_alarms_all = APIRouter()
file_path = os.path.join(Config.HOURLY_PREDICTIONS_PATH, f"{current_time}.parquet")


def get_prediction_for_all_hours(region="all"):
    prediction_now = pd.read_parquet(file_path)

    result = {
        "last_prediction_time": f"{current_time}:00",
        "regions_forecast": {}
    }

    prediction_now['time'] = pd.to_datetime(prediction_now['datetime']).dt.strftime('%H:%M')

    grouped = prediction_now.groupby('city_address')

    if region == "all":
        cities = grouped.groups.keys()
    else:
        if region not in grouped.groups:
            raise ValueError(f"Region '{region}' not in prediction data.")
        cities = region

    for city in cities:
        city_data = grouped.get_group(city)
        forecast = dict(zip(city_data['time'], city_data['predict'].astype(bool)))
        result["regions_forecast"][city] = forecast
    return result


@router_alarms_all.get('/alarms/all')
async def prediction(
    city: str = Header(...),
    key: str = Header(...)
):
    key_check(key)
    return {"prediction": get_prediction_for_all_hours(city),
            "city_address": city}
