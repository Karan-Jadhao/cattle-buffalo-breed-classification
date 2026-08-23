from fastapi import HTTPException, UploadFile


class ImageService:

    ALLOWED_CONTENT_TYPES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    async def read_image(self, file: UploadFile) -> tuple[bytes, str]:

        if file.content_type not in self.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG, and WEBP images are supported.",
            )

        data = await file.read()

        if not data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty.",
            )

        if len(data) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Image size must be less than 5 MB.",
            )

        return data, self.ALLOWED_CONTENT_TYPES[file.content_type]