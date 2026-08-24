import uuid

from fastapi import HTTPException

from app.core.database import supabase


BUCKET_NAME = "prediction-images"


class StorageService:

    async def upload_image(
        self,
        image_data: bytes,
        extension: str,
        content_type: str,
    ) -> str:

        filename = f"{uuid.uuid4()}{extension}"

        storage_path = f"uploads/{filename}"

        try:

            supabase.storage \
                .from_(BUCKET_NAME) \
                .upload(
                    storage_path,
                    image_data,
                    {
                        "content-type": content_type,
                    },
                )

            return storage_path

        except Exception as error:

            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload image: {str(error)}",
            )