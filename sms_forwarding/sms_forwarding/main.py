from api.routes.sms_forwarding import (forwarding_router,
                                       verify_my_iphone_router)
from fastapi import FastAPI
from settings.tortoise_settings import init_tortoise as init_db

app = FastAPI()

app.include_router(forwarding_router)
app.include_router(verify_my_iphone_router)

@app.on_event("startup")
async def startup_event():
    await init_db(app)