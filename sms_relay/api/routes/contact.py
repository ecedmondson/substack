from typing import List
from uuid import UUID

from api.base import make_router_prefix_pattern
from api.schema.forwarding.contact import ContactShape
from database.query.base import get_db
from database.query.contact import ContactQueryService
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

contact_router = APIRouter(
    prefix=make_router_prefix_pattern(["contact"]),
    tags=["contact"],
)


@contact_router.get("/", response_model=List[ContactShape])
def list_contacts(session: Session = Depends(get_db)):
    return [ContactShape.model_validate(c) for c in ContactQueryService.all(session)]

@contact_router.get("/{id}", response_model=ContactShape)
def contact_detail(id: UUID, with_config: bool = Query(default=False, description="Include contact rule config"), session: Session = Depends(get_db)):
    contact = ContactQueryService.by_pkid(session, id, with_config=with_config)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactShape.model_validate(contact)

@contact_router.put("/{id}", response_model=ContactShape)
def update_contact(id: UUID, contact_data: ContactShape, session: Session = Depends(get_db)):
    
    updated = ContactQueryService.update(session, id, contact_data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactShape.model_validate(updated)