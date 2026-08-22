import sys
import torch

from PIL import Image
from torchvision import transforms

from model import create_model


# ==========================================
# Configuration
# ==========================================

MODEL_PATH = "models/cattle_breed_model.pth"

IMAGE_SIZE = 224

TOP_K = 5


# ==========================================
# Device
# ==========================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ==========================================
# Image preprocessing
# ==========================================

transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]
    )
])


# ==========================================
# Check command-line argument
# ==========================================

if len(sys.argv) != 2:

    print("\nUsage:")
    print("python predict.py <image_path>")

    print("\nExample:")
    print("python predict.py test_image.jpg")

    sys.exit()


image_path = sys.argv[1]


# ==========================================
# Check image
# ==========================================

try:

    image = Image.open(image_path).convert("RGB")

except Exception as error:

    print(f"\nERROR: Could not open image.")
    print(error)

    sys.exit()


# ==========================================
# Load model checkpoint
# ==========================================

try:

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=device
    )

except FileNotFoundError:

    print(
        f"\nERROR: Model not found at "
        f"'{MODEL_PATH}'"
    )

    print(
        "\nMake sure training has completed "
        "and the model has been saved."
    )

    sys.exit()


# ==========================================
# Get model information
# ==========================================

num_classes = checkpoint["num_classes"]

class_names = checkpoint["class_names"]


# ==========================================
# Create model
# ==========================================

model = create_model(
    num_classes=num_classes
)


# ==========================================
# Load trained weights
# ==========================================

model.load_state_dict(
    checkpoint["model_state_dict"]
)


model = model.to(device)

model.eval()


# ==========================================
# Prepare image
# ==========================================

image_tensor = transform(image)

image_tensor = image_tensor.unsqueeze(0)

image_tensor = image_tensor.to(device)


# ==========================================
# Prediction
# ==========================================

with torch.no_grad():

    outputs = model(image_tensor)

    probabilities = torch.softmax(
        outputs,
        dim=1
    )


# ==========================================
# Get top predictions
# ==========================================

top_k = min(
    TOP_K,
    num_classes
)

top_probabilities, top_indices = torch.topk(
    probabilities,
    top_k,
    dim=1
)


# ==========================================
# Display result
# ==========================================

print("\n" + "=" * 60)
print("CATTLE / BUFFALO BREED PREDICTION")
print("=" * 60)

print(f"\nImage       : {image_path}")

print(
    f"Device      : {device}"
)

print(
    f"Model       : {MODEL_PATH}"
)


print("\nTop Predictions:")
print("-" * 60)


for i in range(top_k):

    index = top_indices[0][i].item()

    probability = (
        top_probabilities[0][i].item()
        * 100
    )

    breed = class_names[index]

    print(
        f"{i + 1}. {breed:<35} "
        f"{probability:.2f}%"
    )


# ==========================================
# Final prediction
# ==========================================

predicted_index = top_indices[0][0].item()

predicted_breed = class_names[
    predicted_index
]

confidence = (
    top_probabilities[0][0].item()
    * 100
)


print("\n" + "=" * 60)

print(
    f"Predicted Breed : {predicted_breed}"
)

print(
    f"Confidence      : {confidence:.2f}%"
)

print("=" * 60)