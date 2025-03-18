from dotenv import load_dotenv
from os import environ

ROOT_PATH = './../.env'
load_dotenv(ROOT_PATH)


class Config:
    TEST_SECRET = environ.get('TEST_SECRET')

