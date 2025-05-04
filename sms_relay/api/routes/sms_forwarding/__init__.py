from uuid import UUID

from api.base import make_router_prefix_pattern
from api.security.verify_my_iphone import verify_my_iphone_request
from database.models.forwarding.message import (ForwardedMessage,
                                                    MessageRequest,
                                                    MessageResponse)
from database.query.message import ForwardedMessageQueryService
from database.query.base  import get_db
from fastapi import APIRouter, Depends

forwarding_router = APIRouter(
    prefix=make_router_prefix_pattern(["forwarding"]),
    tags=["forwarding"],
)

verify_my_iphone_router = APIRouter(
    prefix=make_router_prefix_pattern(["forwarding"]),
    tags=["forwarding"],
    dependencies=[Depends(verify_my_iphone_request)]
)

forwarding_router.include_router(verify_my_iphone_router)

@verify_my_iphone_router.post("/message", response_model=MessageResponse)
def iphone_automation_hook(
    sms_message: MessageRequest, session = Depends(get_db)
) -> MessageResponse:
    message = ForwardedMessageQueryService().create_forwarded_message(session, sms_message)
    return MessageResponse.model_validate(message)

@forwarding_router.get("/message/{id}", response_model=MessageResponse)
def message_detail(id: UUID) -> MessageResponse:
    return MessageResponse.model_validate(ForwardedMessageQueryService.by_pkid(session, id))