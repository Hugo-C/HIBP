from typing import Annotated

from fastapi import APIRouter, FastAPI, Path

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


@v1_router.get("/haveibeenrocked/{prefix}")
def check_password_leak(prefix: APIPrefix):
    return {"Hello": "World"}


app = FastAPI()
app.include_router(v1_router)
