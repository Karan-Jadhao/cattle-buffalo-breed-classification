from fastapi import APIRouter

from app.core.database import supabase


router = APIRouter()


@router.get("/")
async def health_check():

    try:
        supabase.table("predictions").select(
            "id"
        ).limit(1).execute()

        database_status = "connected"

    except Exception as error:
        database_status = f"error: {str(error)}"

    return {
        "status": "healthy",
        "database": database_status,
    }