from pydantic import SecretStr
from pydantic_settings import BaseSettings


class TelnyxSettings(BaseSettings):
    TELNYX_API_KEY: SecretStr = SecretStr("SUPER-SECRET-KEY")

