
from api.routes.contact import contact_router
from api.routes.relay_rule import relay_router
from api.routes.sms_forwarding import (forwarding_router,
                                       verify_my_iphone_router)
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from settings.server_settings import ServerSettings

app = FastAPI()


##### Server side observability

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error for request {request.url}: {exc.errors()}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

#### For handling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ServerSettings().origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###### Routing
app.include_router(forwarding_router)
app.include_router(verify_my_iphone_router)
app.include_router(contact_router)
app.include_router(relay_router)