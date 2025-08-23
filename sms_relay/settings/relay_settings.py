from pydantic import SecretStr
from pydantic_settings import BaseSettings


class TelnyxSettings(BaseSettings):
    TELNYX_API_KEY: SecretStr = SecretStr("SUPER-SECRET-KEY")
    TELNYX_DEFAULT_NUMBER: str = "867-5309"
    TELNYX_DEFAULT_PROFILE: str = "SMS_RELAY"

