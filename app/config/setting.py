from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_db_url: str
    prod_db: str
    command_bot_token: str
    event_bot_token: str
    gc_config: str
    dashboard_url: str
    is_test: bool = False

    model_config = ConfigDict(env_file="backend/app/.env", env_file_encoding="utf-8")


settings = Settings()
