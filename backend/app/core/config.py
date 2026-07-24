from __future__ import annotations

import os


class Settings:
    api_v1_prefix = "/api/v1"
    database_url = os.getenv("DATABASE_URL", "sqlite:///./loreforge.sqlite3")
    secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
    access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    cors_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if origin.strip()]


settings = Settings()
