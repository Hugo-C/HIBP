from pydantic import RedisDsn
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    kvrocks_url: RedisDsn = RedisDsn("redis://localhost:6666")
