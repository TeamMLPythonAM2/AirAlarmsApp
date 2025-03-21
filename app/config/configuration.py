from dotenv import load_dotenv
from os import environ

load_dotenv()


class Config:
    TEST_SECRET = environ.get('TEST_SECRET')

