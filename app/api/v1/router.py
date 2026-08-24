from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import inference
from app.api.v1.endpoints import prediction


router = APIRouter()


router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)


router.include_router(
    prediction.router,
    prefix="/predictions",
    tags=["Predictions"],
)

router.include_router(inference.router, tags=["Inference"])
