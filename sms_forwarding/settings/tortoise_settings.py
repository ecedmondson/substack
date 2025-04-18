from fastapi import FastAPI
from settings.connection_settings import DBConnectionSettings
from settings.models_settings import ModelSettings
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

db_settings = DBConnectionSettings()
model_settings = ModelSettings()

class RouterSettings:
    def db_for_read(self, *args, **kwargs):
        return "default"
    
    def db_for_write(self, *args, **kwargs):
        return "default"

TORTOISE_ORM = {
    "connections": {"default": db_settings.url},
    "apps": {
        "models": {
            "models": model_settings.model_registry,
            "default_connection": "default",
        },
    },
}

async def init_tortoise(fastapi_app: FastAPI) -> None:
    register_tortoise(
        fastapi_app,
        generate_schemas=False,
    )
    await Tortoise.init(
        db_url=db_settings.url,
        modules={'models': model_settings.project_models}
    )


