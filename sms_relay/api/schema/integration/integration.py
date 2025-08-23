
from api.schema.mixins.primary_key import UUIDPrimaryKeyPydanticMixin


class IntegrationContactSummary(UUIDPrimaryKeyPydanticMixin):
    provider: str
    source: str = "internal"
