from uuid import UUID

from api.base import make_router_prefix_pattern
from api.security.verify_my_iphone import verify_my_iphone_request
from database.models.sms_forwarding.message import (ForwardedMessage,
                                                    MessageRequest,
                                                    MessageResponse)
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
async def iphone_automation_hook(sms_message: MessageRequest) -> MessageResponse:
    message = await sms_message.create_forwarded_message()
    return await MessageResponse.from_tortoise(message)

@forwarding_router.get("/message/{id}", response_model=MessageResponse)
async def message_detail(id: UUID) -> MessageResponse:
    return await ForwardedMessage.get(id=id)