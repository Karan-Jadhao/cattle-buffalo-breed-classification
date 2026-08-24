from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.services.model_service import InvalidImageError, ModelLoadError, model_service


router = APIRouter()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/predict")
async def predict(image: UploadFile | None = File(default=None)) -> dict:
    """Classify one JPEG or PNG without persisting the uploaded image."""
    if image is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An image file is required.")

    suffix = f".{image.filename.rsplit('.', 1)[-1].lower()}" if image.filename and "." in image.filename else ""
    if image.content_type not in ALLOWED_CONTENT_TYPES or suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG and PNG images are supported.",
        )

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded image is empty.")
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Image must be 5 MB or smaller.")

    try:
        result = model_service.predict(image_bytes)
    except InvalidImageError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except ModelLoadError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The classification model is currently unavailable.",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction could not be completed. Please try again.",
        ) from None
    finally:
        await image.close()

    return {"success": True, **result}
