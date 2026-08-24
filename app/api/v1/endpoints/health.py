from fastapi import APIRouter

from app.core.database import supabase
from app.services.model_service import model_service


router = APIRouter()


@router.get("")
async def health_check():

    try:
        supabase.table("predictions").select(
            "id"
        ).limit(1).execute()

        database_status = "connected"

    except Exception as error:
        database_status = f"error: {str(error)}"

    return {
        "status": "healthy" if model_service.load_error is None else "degraded",
        "database": database_status,
        "model": "ready" if model_service.model is not None else "unavailable",
    }
