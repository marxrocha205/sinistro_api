import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")

settings = Settings()
