from fastapi import APIRouter, Header, HTTPException
from datetime import datetime, timedelta
import pandas as pd
from app.config.configuration import Config
from app.utils.key_verification import key_check
import os

router_get = APIRouter()


def get_prediction(city, hour) -> bool:
    try:
        datetime_now = datetime.now(tz=Config.KYIV_TZ).replace(minute=0, second=0, microsecond=0)
        path_time = datetime_now.strftime("%Y-%m-%d_%H")
        file_path = os.path.join(Config.HOURLY_PREDICTIONS_PATH, f"{path_time}.parquet")
        prediction_now = pd.read_parquet(file_path)
        required_time = datetime_now + timedelta(hours=hour)
        required_time = required_time.replace(tzinfo=None)
        prediction_now['datetime'] = prediction_now['datetime'].dt.tz_localize(None)
        data_to_return = ((prediction_now[(prediction_now['city_address'] == city) &
                                          (prediction_now['datetime'] == required_time)]
                          .get("predict")))
        return bool(data_to_return.values[0])
    except Exception as e:
        raise HTTPException(status_code=403, detail="Access forbidden")


@router_get.get('/prediction')
async def prediction(
    city: str = Header(...),
    hour: int = Header(...),
    key: str = Header(...)
):
    key_check(key)
    return {"prediction": get_prediction(city, hour),
            "city_address": city,
            "hour_to_add": hour}


if __name__ == "__main__":
    print(get_prediction('Kyiv', 1))
