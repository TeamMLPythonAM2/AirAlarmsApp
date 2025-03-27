import logging
from functools import wraps
import os

from fastapi import Request, Response, status, HTTPException
import datetime as dt

PATH: str = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger("logger")
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    log_format = '[%(asctime)s] [%(levelname)s] [%(module)s.%(funcName)s] - %(message)s'
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(os.path.join(PATH, '{:%Y_%m_%d}.log'.format(dt.datetime.now())))
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def log_date():
    return dt.datetime.now().strftime("%Y_%m_%d")


def log_base(request: Request, response: Response) -> str:
    return (f'{request.method}: {request.url}: {request.query_params or "NO_PARAMS"}  '
            f'>> {response.status_code}')


def loggable(endpoint):
    @wraps(endpoint)
    async def wrapper(request: Request = None, response: Response = None, *args, **kwargs):
        result = "None"
        try:
            result = await endpoint(request, response, *args, **kwargs)
        except HTTPException as e:
            response.status_code = e.status_code
            result = e.detail
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            result = str(e)
        finally:
            logger.info(f'{log_base(request, response)} >> {result}')
            return result
    return wrapper
