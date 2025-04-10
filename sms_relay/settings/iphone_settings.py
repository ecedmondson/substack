from pydantic import SecretStr
from pydantic_settings import BaseSettings


class MyIphoneSettings(BaseSettings):
    MY_IPHONE_SECRET_HEADER_KEY: SecretStr = SecretStr("X-Iphone-Secret")
    MY_IPHONE_SECRET_HEADER_VALUE: SecretStr = SecretStr("iphonesecretvalue")

    @property
    def expected_header_key(self) -> str:
        return self.MY_IPHONE_SECRET_HEADER_KEY.get_secret_value()

    @property
    def expected_header_value(self) -> str:
        return self.MY_IPHONE_SECRET_HEADER_VALUE.get_secret_value()
