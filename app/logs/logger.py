import logging
from functools import wraps

from fastapi import Request

logging.basicConfig(
    filename='./logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def loggable(endpoint):
    @wraps(endpoint)
    async def wrapper(request: Request = None, *args, **kwargs):
        try:
            response: dict = await endpoint(request, *args, **kwargs)
            logging.info(f'{request.method} : {request.url} >> {response.get("status_code")} >> {response.get("content")}')
            return response
        except Exception as e:
            logging.error(f'{request.method} : {request.url} >> {e}')
    return wrapper
