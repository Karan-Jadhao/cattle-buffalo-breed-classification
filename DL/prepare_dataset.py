import os
import pandas as pd

from sklearn.model_selection import train_test_split


# ==========================================
# Configuration
# ==========================================

DATASET_PATH = "cattle"

OUTPUT_PATH = "data"

IMAGE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

RANDOM_STATE = 42


# ==========================================
# Check dataset
# ==========================================

if not os.path.exists(DATASET_PATH):

    print(f"ERROR: '{DATASET_PATH}' folder not found.")
    exit()


# ==========================================
# Get breed folders
# ==========================================

breeds = sorted([
    folder
    for folder in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, folder))
])


print("=" * 70)
print("DATASET PREPARATION")
print("=" * 70)

print(f"Number of breeds: {len(breeds)}")


# ==========================================
# Create image dataframe
# ==========================================

data = []

for breed in breeds:

    breed_path = os.path.join(
        DATASET_PATH,
        breed
    )

    for image_name in os.listdir(breed_path):

        if image_name.lower().endswith(IMAGE_EXTENSIONS):

            image_path = os.path.join(
                breed_path,
                image_name
            )

            data.append({
                "image_path": image_path,
                "breed": breed
            })


df = pd.DataFrame(data)


print(f"Total images: {len(df)}")


# ==========================================
# Create label IDs
# ==========================================

class_names = sorted(df["breed"].unique())

class_to_index = {
    breed: index
    for index, breed in enumerate(class_names)
}

df["label"] = df["breed"].map(class_to_index)


print("\nClass mapping:")

for breed, index in class_to_index.items():

    print(f"{index:2d} -> {breed}")


# ==========================================
# First split
# 70% training
# 30% temporary
# ==========================================

train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    stratify=df["label"],
    random_state=RANDOM_STATE
)


# ==========================================
# Second split
# 15% validation
# 15% testing
# ==========================================

val_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    stratify=temp_df["label"],
    random_state=RANDOM_STATE
)


# ==========================================
# Reset indexes
# ==========================================

train_df = train_df.reset_index(drop=True)
val_df = val_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)


# ==========================================
# Create output directory
# ==========================================

os.makedirs(OUTPUT_PATH, exist_ok=True)


# ==========================================
# Save CSV files
# ==========================================

train_df.to_csv(
    os.path.join(OUTPUT_PATH, "train.csv"),
    index=False
)

val_df.to_csv(
    os.path.join(OUTPUT_PATH, "val.csv"),
    index=False
)

test_df.to_csv(
    os.path.join(OUTPUT_PATH, "test.csv"),
    index=False
)


# ==========================================
# Save class names
# ==========================================

class_df = pd.DataFrame({
    "label": list(range(len(class_names))),
    "breed": class_names
})

class_df.to_csv(
    os.path.join(OUTPUT_PATH, "classes.csv"),
    index=False
)


# ==========================================
# Display results
# ==========================================

print("\n" + "=" * 70)
print("SPLIT SUMMARY")
print("=" * 70)

print(f"Training images   : {len(train_df)}")
print(f"Validation images : {len(val_df)}")
print(f"Testing images    : {len(test_df)}")
print(f"Total images      : {len(df)}")


print("\nPercentages:")

print(
    f"Training   : {len(train_df) / len(df) * 100:.2f}%"
)

print(
    f"Validation : {len(val_df) / len(df) * 100:.2f}%"
)

print(
    f"Testing    : {len(test_df) / len(df) * 100:.2f}%"
)


# ==========================================
# Check each split contains all breeds
# ==========================================

print("\n" + "=" * 70)
print("CLASS DISTRIBUTION CHECK")
print("=" * 70)

print("\nTraining:")
print(train_df["breed"].value_counts().sort_index())

print("\nValidation:")
print(val_df["breed"].value_counts().sort_index())

print("\nTesting:")
print(test_df["breed"].value_counts().sort_index())


print("\n" + "=" * 70)
print("DATASET PREPARATION COMPLETE")
print("=" * 70)