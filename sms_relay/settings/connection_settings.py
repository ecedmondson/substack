from pydantic import SecretStr
from pydantic_settings import BaseSettings


class DBConnectionSettings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: SecretStr = SecretStr("password")
    POSTGRES_HOST: str = "localhost"
    POSTGRES_NAME: str = "postgres"
    POSTGRES_PORT: int = 5432

    @property
    def url(self) -> str:
        return f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"