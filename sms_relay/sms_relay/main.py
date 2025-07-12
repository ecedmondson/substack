from api.routes.sms_forwarding import (forwarding_router,
                                       verify_my_iphone_router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings.server_settings import ServerSettings

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ServerSettings().origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(forwarding_router)
app.include_router(verify_my_iphone_router)
