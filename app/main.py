from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router
from app.core.config import settings
from app.services.model_service import ModelLoadError, model_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        model_service.load()
    except ModelLoadError:
        # The API remains available so /health and /docs can report the issue.
        pass
    yield


app = FastAPI(
    title="Cattle Buffalo Breed Classification API",
    description="API for cattle and buffalo breed classification",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "message": "Cattle Buffalo Breed Classification API",
        "status": "running",
    }
