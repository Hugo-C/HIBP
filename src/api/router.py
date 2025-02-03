from typing import Annotated

from fastapi import APIRouter, Path
from redis import Redis

from src.api.dependencies import SettingsDep
from src.common import PasswordStorage

v1_router = APIRouter(
    prefix="/api/v1",
)

PREFIX_REGEX_PATTERN = "^[0-9a-fA-F]{5}$"
APIPrefix = Annotated[
    str,
    Path(
        description="5 first chars of a password hash",
        example="123AB",
        pattern=PREFIX_REGEX_PATTERN,
    ),
]


@v1_router.get("/haveibeenrocked/{prefix}")  # TODO add response schema to openAPI
def check_password_leak(prefix: APIPrefix, settings: SettingsDep):
    redis_client = Redis.from_url(str(settings.kvrocks_url))
    password_storage = PasswordStorage(client=redis_client)

    matching_password = password_storage.get_passwords(prefix=prefix)

    return {prefix: matching_password}
