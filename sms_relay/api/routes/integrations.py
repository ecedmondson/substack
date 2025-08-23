
from api.base import make_router_prefix_pattern
from api.schema.integration.telnyx_webhook import (ExpectedTelnyxWebhookShape,
                                                   TelnyxWebhookCreation)
from database.query.base import get_db
from database.query.integration import IntegrationQueryService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

integration_router = APIRouter(
    prefix=make_router_prefix_pattern(["integration"]),
    tags=["relay", "integration"],
)


@integration_router.post("/telnyx/webhook")
async def webhook(payload: ExpectedTelnyxWebhookShape, session: Session = Depends(get_db)):
    integration = IntegrationQueryService.create(
        session,
        "TELNYX",
        payload.model_dump()
    )
    return TelnyxWebhookCreation.model_validate(integration)

