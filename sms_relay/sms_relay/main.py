from fastapi import FastAPI
from settings.tortoise_settings import init_tortoise as init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db(app)