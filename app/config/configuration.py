from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    TEST_SECRET = environ.get("TEST_SECRET")
