from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_hostname: str
    database_port: str                  
    database_password: str
    database_name: str
    database_username: str
    secret_key: Optional[str]  # Make the field optional
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore
