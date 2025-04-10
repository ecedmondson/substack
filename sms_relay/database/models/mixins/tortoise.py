
from pydantic import BaseModel


class TortoiseModelMixin(BaseModel):
    class Meta:
        orm_model = None

    def create_orm_model(self):
        model_cls = self.Meta.orm_model
        return model_cls.create(**self.model_dump())
