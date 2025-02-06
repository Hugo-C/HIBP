from functools import cache
from typing import Annotated

from fastapi.params import Depends

from src.common import Settings


def get_settings() -> Settings:
    return Settings()


@cache
def get_settings_cached() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings_cached)]
