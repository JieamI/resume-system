from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins = settings.BACKEND_CORS_ORIGINS,
        allow_credentials = True,
        allow_methods = ["POST", "GET"],
        allow_headers = ["*"],
    )

from api.api import api_router
app.include_router(api_router, prefix = settings.API_PREFIX)

    