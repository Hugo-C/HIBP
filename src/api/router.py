from fastapi import APIRouter
from redis import Redis

from src.api.dependencies import SettingsDep
from src.common import Password, PasswordStorage, Prefix

v1_router = APIRouter(
    prefix="/api/v1",
)


@v1_router.get("/haveibeenrocked/{prefix}")
def check_password_leak(prefix: Prefix, settings: SettingsDep) -> dict[Prefix, set[Password]]:
    redis_client = Redis.from_url(str(settings.kvrocks_url))
    password_storage = PasswordStorage(client=redis_client)

    matching_password = password_storage.get_passwords(prefix=prefix)

    return {prefix: matching_password}
