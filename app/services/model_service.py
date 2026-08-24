"""In-process inference for the trained cattle and buffalo breed classifier."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms
from torchvision.models import convnext_tiny, efficientnet_b0

from app.core.config import settings


class ModelLoadError(RuntimeError):
    """Raised when the configured checkpoint cannot be used for inference."""


class InvalidImageError(ValueError):
    """Raised when uploaded bytes are not a readable image."""


class ModelService:
    """Loads one supported classifier checkpoint and serves predictions from it."""

    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model: torch.nn.Module | None = None
        self.class_names: list[str] = []
        self.model_path: Path | None = None
        self.load_error: str | None = None
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

    def load(self) -> None:
        """Load the checkpoint once. Calling this again is harmless."""
        if self.model is not None:
            return

        try:
            path = self._checkpoint_path()
            checkpoint = self._load_checkpoint(path)
            state_dict = self._state_dict(checkpoint)
            class_names = checkpoint.get("class_names")
            if not isinstance(class_names, (list, tuple)) or not class_names:
                raise ModelLoadError("Checkpoint does not contain a non-empty 'class_names' list.")

            num_classes = self._num_classes(checkpoint, state_dict)
            if len(class_names) != num_classes:
                raise ModelLoadError(
                    "Checkpoint class_names length does not match its classifier output size."
                )

            model = self._create_model(checkpoint, state_dict, num_classes)
            model.load_state_dict(state_dict, strict=True)
            self.model = model.to(self.device).eval()
            self.class_names = [str(name) for name in class_names]
            self.model_path = path
            self.load_error = None
        except Exception as error:
            self.load_error = str(error)
            if isinstance(error, ModelLoadError):
                raise
            raise ModelLoadError("Unable to load the trained classification model.") from error

    def predict(self, image_bytes: bytes) -> dict[str, Any]:
        if self.model is None:
            try:
                self.load()
            except ModelLoadError as error:
                raise ModelLoadError("The classification model is unavailable.") from error

        image = self._open_image(image_bytes)
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            probabilities = torch.softmax(self.model(tensor), dim=1)
            count = min(5, len(self.class_names))
            values, indices = torch.topk(probabilities, k=count, dim=1)

        top_5 = [
            {
                "breed": self.class_names[index.item()],
                "class_index": index.item(),
                "confidence": round(value.item(), 6),
            }
            for value, index in zip(values[0], indices[0], strict=True)
        ]
        return {"prediction": top_5[0], "top_5": top_5}

    def _checkpoint_path(self) -> Path:
        configured = Path(settings.model_path)
        path = configured if configured.is_absolute() else settings.project_root / configured
        if not path.is_file():
            raise ModelLoadError(f"Configured model checkpoint was not found: {path}")
        return path

    @staticmethod
    def _load_checkpoint(path: Path) -> dict[str, Any]:
        try:
            checkpoint = torch.load(path, map_location="cpu", weights_only=False)
        except TypeError:  # Supports older PyTorch releases.
            checkpoint = torch.load(path, map_location="cpu")
        if not isinstance(checkpoint, dict):
            raise ModelLoadError("Checkpoint must be a dictionary with model metadata.")
        return checkpoint

    @staticmethod
    def _state_dict(checkpoint: dict[str, Any]) -> dict[str, torch.Tensor]:
        state_dict = checkpoint.get("model_state_dict", checkpoint.get("state_dict"))
        if not isinstance(state_dict, dict):
            raise ModelLoadError("Checkpoint does not contain 'model_state_dict' or 'state_dict'.")
        return {
            key.removeprefix("module."): value
            for key, value in state_dict.items()
        }

    @staticmethod
    def _num_classes(checkpoint: dict[str, Any], state_dict: dict[str, torch.Tensor]) -> int:
        value = checkpoint.get("num_classes")
        if isinstance(value, int) and value > 0:
            return value
        for key in ("classifier.2.weight", "classifier.1.weight"):
            weights = state_dict.get(key)
            if weights is not None:
                return int(weights.shape[0])
        raise ModelLoadError("Could not determine the checkpoint's number of classes.")

    @staticmethod
    def _create_model(
        checkpoint: dict[str, Any], state_dict: dict[str, torch.Tensor], num_classes: int
    ) -> torch.nn.Module:
        architecture = str(checkpoint.get("architecture", "")).lower()
        if "efficientnet" in architecture or "classifier.1.weight" in state_dict:
            model = efficientnet_b0(weights=None)
            model.classifier[-1] = torch.nn.Linear(model.classifier[-1].in_features, num_classes)
            return model
        if "convnext" in architecture or "classifier.2.weight" in state_dict:
            model = convnext_tiny(weights=None)
            model.classifier[-1] = torch.nn.Linear(model.classifier[-1].in_features, num_classes)
            return model
        raise ModelLoadError("Unsupported checkpoint architecture. Expected ConvNeXt-Tiny or EfficientNet-B0.")

    @staticmethod
    def _open_image(image_bytes: bytes) -> Image.Image:
        try:
            with Image.open(BytesIO(image_bytes)) as source:
                source.verify()
            with Image.open(BytesIO(image_bytes)) as source:
                return source.convert("RGB").copy()
        except (UnidentifiedImageError, OSError, ValueError) as error:
            raise InvalidImageError("The uploaded file is not a valid image.") from error


model_service = ModelService()
