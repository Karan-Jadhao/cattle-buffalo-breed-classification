from app.core.database import supabase


class PredictionService:

    async def create_prediction(
        self,
        image_path: str,
    ):

        data = {
            "image_path": image_path,
            "predicted_breed": None,
            "confidence": None,
            "model_version": None,
        }

        response = (
            supabase
            .table("predictions")
            .insert(data)
            .execute()
        )

        return response.data[0]

    async def update_prediction(
        self,
        prediction_id: str,
        predicted_breed: str,
        confidence: float,
        model_version: str = "v1",
    ):

        data = {
            "predicted_breed": predicted_breed,
            "confidence": confidence,
            "model_version": model_version,
            "status": "completed",
        }

        response = (
            supabase
            .table("predictions")
            .update(data)
            .eq("id", prediction_id)
            .execute()
        )

        return response.data[0]

    async def mark_failed(
    self,
    prediction_id: str,
   ):
        response = (
            supabase
            .table("predictions")
            .update({
                "status": "failed"
            })
            .eq("id", prediction_id)
            .execute()
        )

        return response.data[0]