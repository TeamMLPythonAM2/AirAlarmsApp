from fastapi import FastAPI, APIRouter, Header
from app.core.data_processing.hourly_predict import predict


router_predict = APIRouter()


@router_predict.get('/update_predictions')
async def update_predictions():
    try:
        await predict()
        return {'access': True}
    except Exception as e:
        return {'access': False, 'error': str(e)}
