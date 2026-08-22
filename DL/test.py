import os
import torch
import torch.nn as nn
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

import matplotlib.pyplot as plt

from dataset import test_loader
from model import create_model


# ==========================================
# Configuration
# ==========================================

MODEL_PATH = "models/cattle_breed_model.pth"

RESULTS_DIR = "results"


# ==========================================
# Device
# ==========================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 70)
print("CATTLE & BUFFALO BREED MODEL TESTING")
print("=" * 70)

print(f"\nDevice: {device}")


# ==========================================
# Load checkpoint
# ==========================================

if not os.path.exists(MODEL_PATH):

    print(f"\nERROR: Model not found:")
    print(MODEL_PATH)
    print("\nTrain the model first.")
    exit()


checkpoint = torch.load(
    MODEL_PATH,
    map_location=device
)


# ==========================================
# Get model information
# ==========================================

num_classes = checkpoint["num_classes"]

class_names = checkpoint["class_names"]

best_val_accuracy = checkpoint[
    "best_val_accuracy"
]


print(f"Number of classes : {num_classes}")

print(
    f"Best validation accuracy : "
    f"{best_val_accuracy:.2f}%"
)


# ==========================================
# Create model
# ==========================================

model = create_model(
    num_classes=num_classes
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(device)

model.eval()


# ==========================================
# Testing
# ==========================================

all_labels = []
all_predictions = []

top5_correct = 0
total_samples = 0


with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)
        labels = labels.to(device)


        # Forward pass
        outputs = model(images)


        # Top-1 prediction
        _, predictions = torch.max(
            outputs,
            1
        )


        # Store results
        all_labels.extend(
            labels.cpu().numpy()
        )

        all_predictions.extend(
            predictions.cpu().numpy()
        )


        # ----------------------------------
        # Top-5 accuracy
        # ----------------------------------

        top5_predictions = torch.topk(
            outputs,
            k=5,
            dim=1
        ).indices


        for i in range(labels.size(0)):

            if labels[i] in top5_predictions[i]:

                top5_correct += 1


        total_samples += labels.size(0)


# ==========================================
# Convert to NumPy
# ==========================================

all_labels = np.array(all_labels)

all_predictions = np.array(
    all_predictions
)


# ==========================================
# Calculate metrics
# ==========================================

accuracy = accuracy_score(
    all_labels,
    all_predictions
)

precision = precision_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)

top5_accuracy = (
    top5_correct / total_samples
)


# ==========================================
# Print results
# ==========================================

print("\n" + "=" * 70)
print("FINAL TEST RESULTS")
print("=" * 70)

print(
    f"\nTest Accuracy     : {accuracy * 100:.2f}%"
)

print(
    f"Top-5 Accuracy    : {top5_accuracy * 100:.2f}%"
)

print(
    f"Precision         : {precision:.4f}"
)

print(
    f"Recall            : {recall:.4f}"
)

print(
    f"F1 Score          : {f1:.4f}"
)


# ==========================================
# Classification report
# ==========================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

report = classification_report(
    all_labels,
    all_predictions,
    labels=list(range(num_classes)),
    target_names=class_names,
    zero_division=0
)

print(report)


# ==========================================
# Save classification report
# ==========================================

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)

with open(
    os.path.join(
        RESULTS_DIR,
        "classification_report.txt"
    ),
    "w"
) as file:

    file.write(
        f"Test Accuracy: {accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Top-5 Accuracy: "
        f"{top5_accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Precision: {precision:.4f}\n"
    )

    file.write(
        f"Recall: {recall:.4f}\n"
    )

    file.write(
        f"F1 Score: {f1:.4f}\n\n"
    )

    file.write(report)


# ==========================================
# Confusion matrix
# ==========================================

cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=list(range(num_classes))
)


# ==========================================
# Plot confusion matrix
# ==========================================

plt.figure(
    figsize=(24, 20)
)

plt.imshow(
    cm,
    interpolation="nearest"
)

plt.title(
    "Cattle & Buffalo Breed Confusion Matrix"
)

plt.colorbar()

plt.xlabel(
    "Predicted Breed"
)

plt.ylabel(
    "Actual Breed"
)

plt.xticks(
    range(num_classes),
    class_names,
    rotation=90,
    fontsize=6
)

plt.yticks(
    range(num_classes),
    class_names,
    fontsize=6
)

plt.tight_layout()


plt.savefig(
    os.path.join(
        RESULTS_DIR,
        "confusion_matrix.png"
    ),
    dpi=200
)

plt.close()


# ==========================================
# Final
# ==========================================

print("\n" + "=" * 70)

print("TESTING COMPLETE")

print("=" * 70)

print(
    "\nClassification report saved to:"
)

print(
    "results/classification_report.txt"
)

print(
    "\nConfusion matrix saved to:"
)

print(
    "results/confusion_matrix.png"
)

print("\n" + "=" * 70)