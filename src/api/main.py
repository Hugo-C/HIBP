from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .router import v1_router

app = FastAPI()
app.include_router(v1_router)


@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
