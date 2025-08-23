from datetime import datetime
from typing import List
from uuid import UUID
from zoneinfo import ZoneInfo

from api.base import make_router_prefix_pattern
from api.schema.conversation.thread import (ConversationResponse,
                                            ConversationThread)
from api.schema.forwarding.message import (MessageResponse,
                                           MessageThreadResponse,
                                           OutgoingMessage)
from database.query.base import get_db
from database.query.message import ForwardedMessageQueryService
from database.query.thread import ConversationThreadQueryService
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

conversation_router = APIRouter(
    prefix=make_router_prefix_pattern(["conversation"]),
    tags=["conversation"],
)


@conversation_router.get("/thread", response_model=List[ConversationThread])
def fetch_threads(
    page: int = Query(0, ge=0),
    page_size: int = Query(15, ge=1, le=200),
    session: Session = Depends(get_db)
) -> List[ConversationThread]:
    return [ConversationThread.model_validate(thread) for thread in ConversationThreadQueryService.summaries(session, page=page, page_size=page_size)]

@conversation_router.post("/thread/{thread_id}", response_model=MessageResponse)
def respond_to_thread(
    thread_id: str,
    payload: ConversationResponse,
    session: Session = Depends(get_db)
) -> MessageResponse:
    outgoing_message = OutgoingMessage(
        message=payload.message_body,
        sender=payload.phone_number_used,
        integration_contact_id=payload.integration_contact_id,
        date=datetime.now(tz=ZoneInfo('UTC')),
        thread_id=thread_id,
    )
    message = ForwardedMessageQueryService.create_integration_message(session, outgoing_message)
    return MessageResponse.model_validate(message)
    
@conversation_router.get("/thread/{thread_id}", response_model=List[MessageThreadResponse])
def fetch_messages_by_thread(
    thread_id: UUID,
    page: int = Query(0, ge=0),
    page_size: int = Query(25, ge=1, le=200),
    session: Session = Depends(get_db),
) -> List[MessageThreadResponse]:
    conversation = [
        MessageThreadResponse.model_validate(message) for message in ForwardedMessageQueryService.message_thread(
            session, thread_id, offset=page, page_size=page_size
        )
    ]
    return conversation
