from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    postgres_url: str
    secret_key: str
    hash_algorithm: str = 'HS256'


settings = Settings()
