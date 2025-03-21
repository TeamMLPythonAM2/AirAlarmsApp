from dotenv import load_dotenv
from os import environ

ROOT_PATH = './../.env'
load_dotenv(ROOT_PATH)


class Config:
    API_ID: int = environ.get('API_ID')
    API_HASH: str = environ.get('API_HASH')
    API_PHONE: str = environ.get('API_PHONE')
