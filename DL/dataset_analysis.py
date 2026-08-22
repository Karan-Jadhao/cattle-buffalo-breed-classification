import os
from PIL import Image

# ==========================================
# Configuration
# ==========================================

DATASET_PATH = "cattle"

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

# ==========================================
# Check dataset
# ==========================================

if not os.path.exists(DATASET_PATH):
    print(f"ERROR: Dataset folder '{DATASET_PATH}' not found.")
    exit()

# Get breed folders
breeds = sorted([
    folder
    for folder in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, folder))
])

print("=" * 70)
print("CATTLE & BUFFALO BREED DATASET ANALYSIS")
print("=" * 70)

print(f"\nDataset path     : {DATASET_PATH}")
print(f"Number of breeds : {len(breeds)}")

# ==========================================
# Analyze breeds
# ==========================================

total_images = 0
corrupt_images = []
breed_counts = {}

print("\nImages per breed")
print("-" * 70)

for breed in breeds:

    breed_path = os.path.join(DATASET_PATH, breed)

    images = [
        file
        for file in os.listdir(breed_path)
        if file.lower().endswith(IMAGE_EXTENSIONS)
    ]

    breed_counts[breed] = len(images)
    total_images += len(images)

    # Check every image
    for image_name in images:

        image_path = os.path.join(
            breed_path,
            image_name
        )

        try:
            with Image.open(image_path) as image:
                image.verify()

        except Exception:
            corrupt_images.append(image_path)

    print(f"{breed:<45} {len(images):>5}")

# ==========================================
# Dataset statistics
# ==========================================

print("\n" + "=" * 70)
print("DATASET SUMMARY")
print("=" * 70)

print(f"Total breeds     : {len(breeds)}")
print(f"Total images     : {total_images}")

if breed_counts:

    counts = list(breed_counts.values())

    print(f"Minimum images   : {min(counts)}")
    print(f"Maximum images   : {max(counts)}")
    print(f"Average images   : {sum(counts) / len(counts):.2f}")

# ==========================================
# Find breeds with very few images
# ==========================================

print("\n" + "=" * 70)
print("BREEDS WITH LESS THAN 99 IMAGES")
print("=" * 70)

low_image_breeds = [
    (breed, count)
    for breed, count in breed_counts.items()
    if count < 99
]

if not low_image_breeds:
    print("None")
else:
    for breed, count in low_image_breeds:
        print(f"{breed:<45} {count}")

# ==========================================
# Corrupt images
# ==========================================

print("\n" + "=" * 70)
print("CORRUPT IMAGE CHECK")
print("=" * 70)

if not corrupt_images:
    print("No corrupt images found.")
else:

    print(f"Found {len(corrupt_images)} corrupt images:\n")

    for image_path in corrupt_images:
        print(image_path)

# ==========================================
# Empty folders
# ==========================================

print("\n" + "=" * 70)
print("EMPTY BREED FOLDERS")
print("=" * 70)

empty_breeds = [
    breed
    for breed, count in breed_counts.items()
    if count == 0
]

if not empty_breeds:
    print("None")
else:
    for breed in empty_breeds:
        print(breed)

# ==========================================
# Finish
# ==========================================

print("\n" + "=" * 70)
print("DATASET ANALYSIS COMPLETE")
print("=" * 70)