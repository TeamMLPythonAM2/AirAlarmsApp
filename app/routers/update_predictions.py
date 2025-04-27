from fastapi import FastAPI, APIRouter, Header
from app.core.hourly_predict import predict
from app.utils.key_verification import key_check


router_predict = APIRouter()


@router_predict.get('/update_predictions')
async def update_predictions(
    key: str = Header(...)
):
    key_check(key)
    try:
        await predict()
        return {'access': True}
    except Exception as e:
        return {'access': False, 'error': str(e)}
