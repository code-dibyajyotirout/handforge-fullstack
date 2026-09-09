import os

class Settings:
    PROJECT_NAME: str = "HandForge Distributed Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://handforge.app",
        "https://*.workers.dev"
    ]

settings = Settings()
