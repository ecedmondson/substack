
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from api.schema.integration.telnyx_webhook import TelnyxPayloadToMessage
from database.models.relay.integration_relay import (IntegrationContact,
                                                     IntegrationPayload)
from database.query.message import ForwardedMessageQueryService
from database.query.thread import ConversationThreadQueryService
from sqlalchemy import event, select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

@event.listens_for(IntegrationPayload, "after_insert")
def integration_created_listener(mapper, connection, integration_payload):
    payload = integration_payload.payload
    session = Session(bind=connection)
    try:
        integration_contact = IntegrationContactQueryService.by_address(session, payload['to_number'])
        message = ForwardedMessageQueryService.create_forwarded_message(
            session,
            # I can assume this for now since there is only one integration configured
            TelnyxPayloadToMessage(
                message=payload['message_body'],
                sender=payload['from_number'],
                date=datetime.now(tz=ZoneInfo("America/Chicago")),
                relayed=True,
                integration=integration_payload.id,
                integration_contact_id=integration_contact.id,
            )
        )
        thread = ConversationThreadQueryService.create(session, integration_contact.id, message.contact.id, payload['from_number'])
        ForwardedMessageQueryService.assign_thread(session, message.id, thread.id)
    except Exception as e:
        base = f"- Failed to create forwarded message from integration payload. PKID: {integration_payload.id}."
        type_error = f"- Type: {type(e)}"
        message_error = f"- Message: {str(e)}"
        logger.error("Error:\n\t" + base + type_error + message_error)


class IntegrationQueryService:
    @classmethod
    def flush_to_session(cls, session: Session, provider: str, payload: dict) -> IntegrationPayload:
        integration = IntegrationPayload(
            provider=provider,
            payload=payload,
        )
        session.add(integration)
        session.flush()
        return integration

    @classmethod
    def create(cls, session: Session, provider: str, payload: dict) -> IntegrationPayload:
        integration = cls.flush_to_session(session, provider, payload)
        session.commit()
        session.refresh(integration)
        return integration

class IntegrationContactQueryService:
    @classmethod
    def by_address(cls, session: Session, address: str):
        # Once there is more than one integration configured, will likely want to filter
        # by address and provider
        return session.execute(
            select(IntegrationContact).where(IntegrationContact.address == address)
        ).scalar_one_or_none()