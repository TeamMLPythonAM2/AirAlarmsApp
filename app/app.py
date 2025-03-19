from core.services.ExampleService import ExampleService, WeatherDTO
from config import *
from fastapi import FastAPI
import uvicorn

CONFIG = Config()
app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
