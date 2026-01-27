"""
config.py
---------
Central place for application configuration.

- Loads environment variables from `.env`
- Uses Pydantic for validation and type safety
- Fails fast if required settings (like DATABASE_URL) are missing
- Keeps secrets and environment-specific values out of source code

Access settings anywhere via:
    from app.core.config import settings
"""


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "super-secret-dev-key-change-later"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()


