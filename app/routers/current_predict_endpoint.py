from fastapi import FastAPI, APIRouter, Header
from datetime import datetime, timedelta
import pandas as pd
from app.config.configuration import Config
import os

router_get = APIRouter()
file_path = os.path.join(Config.HOURLY_PREDICTIONS_PATH, "predict.parquet")


def get_prediction(city, hour) -> bool:
    prediction_now = pd.read_parquet(file_path)
    print(city, hour)
    datetime_now = datetime.now(tz=Config.KYIV_TZ).replace(minute=0, second=0, microsecond=0)
    required_time = datetime_now + timedelta(hours=hour)
    required_time = required_time.replace(tzinfo=None)
    prediction_now['datetime'] = prediction_now['datetime'].dt.tz_localize(None)
    data_to_return = ((prediction_now[(prediction_now['city_address'] == city) &
                                      (prediction_now['datetime'] == required_time)]
                      .get("predict")))
    return bool(data_to_return.values[0])


@router_get.get('/prediction')
async def prediction(
    city: str = Header(...),
    hour: int = Header(...),
    # key: str = Header(...)
):
    return {"prediction": get_prediction(city, hour),
            "city_address": city,
            "hour_to_add": hour}


if __name__ == "__main__":
    print(get_prediction('Kyiv', 1))
