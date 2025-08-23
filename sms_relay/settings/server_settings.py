from pydantic_settings import BaseSettings


class ServerSettings(BaseSettings):
    @property
    def origins(self) -> list:
        return [
            # Default port on npm run dev
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            # Default port on npm run preview
            "http://127.0.0.1:4173",
            "http://localhost:4173",
            # Port exposed on integration tests
            "http://127.0.0.1:8080",
            "http://localhost:8080",
            "http://frontend",
        ]