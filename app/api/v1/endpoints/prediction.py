from fastapi import APIRouter, File, UploadFile

from app.schemas.prediction import PredictionResponse
from app.services.image_service import ImageService
from app.services.storage_service import StorageService
from app.services.prediction_service import PredictionService
from app.services.dl_service import DLService


router = APIRouter()

image_service = ImageService()
storage_service = StorageService()
prediction_service = PredictionService()
dl_service = DLService()


@router.post(
    "/",
    response_model=PredictionResponse,
)
async def create_prediction(
    image: UploadFile = File(...),
):

    # 1. Validate and read image
    image_data, extension = await image_service.read_image(
        image
    )

    # 2. Upload original image
    image_path = await storage_service.upload_image(
        image_data=image_data,
        extension=extension,
        content_type=image.content_type,
    )

    # 3. Create pending database record
    prediction = await prediction_service.create_prediction(
        image_path=image_path
    )

    prediction_id = str(prediction["id"])

    try:

        result = await dl_service.predict(
            image_path
        )

        updated_prediction = (
            await prediction_service.update_prediction(
                prediction_id=prediction_id,
                predicted_breed=result["predicted_breed"],
                confidence=result["confidence"],
            )
        )

        return PredictionResponse(
            success=True,
            prediction_id=prediction_id,
            image_path=updated_prediction["image_path"],
            predicted_breed=updated_prediction["predicted_breed"],
            confidence=updated_prediction["confidence"],
            model_version=updated_prediction["model_version"],
            status=updated_prediction["status"],
            message="Prediction completed successfully.",
        )

    except Exception:

        await prediction_service.mark_failed(
            prediction_id
        )

        raise