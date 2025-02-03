from typing import Annotated

from fastapi.params import Depends

from src.common import Settings


def get_settings() -> Settings:
    return Settings()


# TODO cache settings + password_storage ?

SettingsDep = Annotated[Settings, Depends(get_settings)]
