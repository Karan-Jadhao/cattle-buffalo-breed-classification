import re
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import HTTPException

from app.core.database import supabase


class DLService:

    BUCKET_NAME = "prediction-images"

    DL_DIR = Path(__file__).resolve().parents[2] / "DL"

    PREDICT_SCRIPT = DL_DIR / "predict.py"

    async def predict(self, image_path: str) -> dict:

        temp_file_path = None

        try:
            # 1. Download image from Supabase Storage
            image_data = (
                supabase.storage
                .from_(self.BUCKET_NAME)
                .download(image_path)
            )

            if not image_data:
                raise HTTPException(
                    status_code=500,
                    detail="Could not download image from storage.",
                )

            # 2. Preserve original extension
            extension = Path(image_path).suffix or ".jpg"

            with NamedTemporaryFile(
                delete=False,
                suffix=extension,
            ) as temp_file:

                temp_file.write(image_data)

                temp_file_path = Path(
                    temp_file.name
                )

            # 3. Make sure predict.py exists
            if not self.PREDICT_SCRIPT.exists():

                raise HTTPException(
                    status_code=500,
                    detail=f"DL prediction script not found: {self.PREDICT_SCRIPT}",
                )

            # 4. Run existing DL prediction script
            result = subprocess.run(
                [
                    sys.executable,
                    str(self.PREDICT_SCRIPT),
                    str(temp_file_path),
                ],
                cwd=str(self.DL_DIR),
                capture_output=True,
                text=True,
                timeout=120,
            )

            # 5. Check if DL process failed
            if result.returncode != 0:

                raise HTTPException(
                    status_code=500,
                    detail=f"DL prediction failed: {result.stderr}",
                )

            # 6. Parse prediction
            return self._parse_output(result.stdout)

        except HTTPException:
            raise

        except subprocess.TimeoutExpired:

            raise HTTPException(
                status_code=504,
                detail="DL prediction timed out.",
            )

        except Exception as error:

            raise HTTPException(
                status_code=500,
                detail=f"DL service error: {str(error)}",
            )

        finally:

            # 7. Delete temporary file
            if temp_file_path and temp_file_path.exists():

                try:
                    temp_file_path.unlink()

                except OSError:
                    pass

    @staticmethod
    def _parse_output(output: str) -> dict:

        breed_match = re.search(
            r"Predicted Breed\s*:\s*(.+)",
            output,
        )

        confidence_match = re.search(
            r"Confidence\s*:\s*([\d.]+)%",
            output,
        )

        if not breed_match or not confidence_match:

            raise HTTPException(
                status_code=503,
                detail={
                    "message": "DL model did not return a prediction.",
                    "dl_output": output,
                },
            )

        predicted_breed = breed_match.group(1).strip()

        confidence = float(
            confidence_match.group(1)
        )

        return {
            "predicted_breed": predicted_breed,
            "confidence": confidence,
        }