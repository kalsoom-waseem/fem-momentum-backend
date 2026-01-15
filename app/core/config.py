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

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()


