
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from api.schema.integration.telnyx_webhook import TelnyxPayloadToMessage
from database.models.relay.integration_relay import IntegrationPayload
from database.query.message import ForwardedMessageQueryService
from sqlalchemy import event
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

@event.listens_for(IntegrationPayload, "after_insert")
def integration_created_listener(mapper, connection, integration_payload):
    payload = integration_payload.payload
    print()
    print(payload)
    print()
    session = Session(bind=connection)
    try:
        ForwardedMessageQueryService.create_forwarded_message(
            session,
            TelnyxPayloadToMessage(
                message=payload['message_body'],
                sender=payload['from_number'],
                date=datetime.now(tz=ZoneInfo("America/Chicago")),
                relayed=True,
                integration=integration_payload.id,
            )
        )
    except Exception as e:
        base = f"- Failed to create forwarded message from integration payload. PKID: {integration_payload.id}."
        type_error = f"- Type: {type(e)}"
        message_error = f"- Message: {str(e)}"
        logger.error("Error:\n\t" + base + type_error + message_error)


class IntegrationQueryService:
    @classmethod
    def add_to_session(cls, session: Session, provider: str, payload: dict) -> IntegrationPayload:
        integration = IntegrationPayload(
            provider=provider,
            payload=payload,
        )
        session.add(integration)
        return integration

    @classmethod
    def create(cls, session: Session, provider: str, payload: dict) -> IntegrationPayload:
        integration = cls.add_to_session(session, provider, payload)
        session.commit()
        session.refresh(integration)
        return integration
    