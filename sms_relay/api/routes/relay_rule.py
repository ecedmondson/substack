from typing import List

from api.base import make_router_prefix_pattern
from api.schema.relay.rule import (ContactRuleConfigShape, CreateRulePayload,
                                   DisableRulePayload, RuleShape)
from database.query.base import get_db
from database.query.contact_rule_config import ContactRuleConfigQueryService
from database.query.rules import ContactRuleQueryService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

relay_router = APIRouter(
    prefix=make_router_prefix_pattern(["relay"]),
    tags=["relay"],
)


@relay_router.get("/rule", response_model=List[RuleShape])
def list_rules(session: Session = Depends(get_db)):
    return [RuleShape.model_validate(c) for c in ContactRuleQueryService.all(session)]

@relay_router.post("/config/rule/enable", response_model=ContactRuleConfigShape)
def add_or_enable_rule_for_contact(
    payload: CreateRulePayload,
    session: Session = Depends(get_db),
):
    try:
        config = ContactRuleConfigQueryService.add_rule_to_config(
            session, payload.config_id, payload.rule_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return ContactRuleConfigShape.model_validate(config)

@relay_router.post("/config/rule/disable")
def disable_rule_for_contact(
    payload: DisableRulePayload,
    session: Session = Depends(get_db),
):
    try:
        config = ContactRuleConfigQueryService.disable_rule_in_config(
            session=session,
            config_id=payload.config_id,
            rule_id=payload.rule_id,
        )
        return ContactRuleConfigShape.model_validate(config)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
