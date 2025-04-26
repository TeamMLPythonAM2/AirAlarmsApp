from fastapi import APIRouter, Header
from datetime import datetime, timedelta
import pandas as pd
from app.config.configuration import Config
from app.utils.key_verification import key_check
import os

# Router just for task 7

router_task_7 = APIRouter()
file_path = os.path.join(Config.HOURLY_PREDICTIONS_PATH, "predict.parquet")


def get_prediction_for_all_hours(region="all"):
    prediction_now = pd.read_parquet(file_path)

    result = {
        "last_prediction_time": "ВСТАВИТИ СЮДИ НАЗВУ ФАЙЛУ!!!",
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


@router_task_7.get('/prediction_7')
async def prediction(
    city: str = Header(...),
    key: str = Header(...)
):
    key_check(key)
    return {"prediction": get_prediction_for_all_hours(city),
            "city_address": city}
