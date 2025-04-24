from app.config.configuration import Config
from fastapi import HTTPException


def key_check(api_key: str):
    if api_key != Config.PREDICTION_KEY:
        raise HTTPException(status_code=403, detail="Wrong API key")
    return True


# def key_ws_check(api_key: str):
#     return api_key == Config.PREDICTION_KEY
