from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kvrocks_url: RedisDsn = RedisDsn("redis://localhost:6666")
