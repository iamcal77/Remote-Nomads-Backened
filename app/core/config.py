from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = Field(..., alias="APP_NAME")
    ENV: str = "development"

    DATABASE_URL: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = {
        "env_file": ".env",
        "extra": "forbid",
        "case_sensitive": False,
    }

settings = Settings()
