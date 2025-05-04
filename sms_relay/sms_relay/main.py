from api.routes.sms_forwarding import (forwarding_router,
                                       verify_my_iphone_router)
from fastapi import FastAPI
from database.query.base  import connection
app = FastAPI()

app.include_router(forwarding_router)
app.include_router(verify_my_iphone_router)
