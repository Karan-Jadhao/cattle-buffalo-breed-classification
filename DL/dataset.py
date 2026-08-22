import pandas as pd
from PIL import Image

import torch
from torch.utils.data import Dataset, DataLoader

from torchvision import transforms


# ==========================================
# Configuration
# ==========================================

IMAGE_SIZE = 224

BATCH_SIZE = 32


# ==========================================
# Training transformations
# ==========================================

train_transform = transforms.Compose([

    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),

    transforms.RandomHorizontalFlip(p=0.5),

    transforms.RandomRotation(10),

    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ==========================================
# Validation/Test transformations
# ==========================================

test_transform = transforms.Compose([

    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ==========================================
# Custom Dataset
# ==========================================

class CattleBreedDataset(Dataset):

    def __init__(self, csv_file, transform=None):

        self.data = pd.read_csv(csv_file)

        self.transform = transform


    def __len__(self):

        return len(self.data)


    def __getitem__(self, index):

        image_path = self.data.iloc[index]["image_path"]

        label = int(self.data.iloc[index]["label"])


        # Load image
        image = Image.open(image_path).convert("RGB")


        # Apply transformation
        if self.transform:

            image = self.transform(image)


        return image, label


# ==========================================
# Create datasets
# ==========================================

train_dataset = CattleBreedDataset(
    "data/train.csv",
    transform=train_transform
)


val_dataset = CattleBreedDataset(
    "data/val.csv",
    transform=test_transform
)


test_dataset = CattleBreedDataset(
    "data/test.csv",
    transform=test_transform
)


# ==========================================
# Create DataLoaders
# ==========================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)


val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


# ==========================================
# Test the pipeline
# ==========================================

if __name__ == "__main__":

    print("=" * 60)
    print("PYTORCH DATA PIPELINE TEST")
    print("=" * 60)

    print(f"\nTraining images   : {len(train_dataset)}")
    print(f"Validation images : {len(val_dataset)}")
    print(f"Testing images    : {len(test_dataset)}")

    # Get one batch
    images, labels = next(iter(train_loader))

    print("\nBatch information:")
    print(f"Image tensor shape : {images.shape}")
    print(f"Label tensor shape : {labels.shape}")

    print("\nFirst image:")
    print(f"Shape : {images[0].shape}")
    print(f"Label : {labels[0].item()}")

    print("\nNumber of batches:")
    print(f"Training   : {len(train_loader)}")
    print(f"Validation : {len(val_loader)}")
    print(f"Testing    : {len(test_loader)}")

    print("\n" + "=" * 60)
    print("DATA PIPELINE WORKING SUCCESSFULLY")
    print("=" * 60)