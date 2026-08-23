from pydantic import BaseModel


class PredictionResponse(BaseModel):

    success: bool

    prediction_id: str

    image_path: str

    predicted_breed: str | None = None

    confidence: float | None = None

    model_version: str | None = None

    status: str

    message: str | None = None