import torch
import torch.nn as nn

from sklearn.metrics import (
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

from dataset import test_loader
from model import create_model


# ==========================================
# Configuration
# ==========================================

MODEL_PATH = (
    "models/efficientnet_b0_cattle_breed_model.pth"
)


# ==========================================
# Device
# ==========================================

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    print("=" * 70)
    print("CATTLE & BUFFALO BREED CLASSIFICATION")
    print("EFFICIENTNET-B0 - TEST")
    print("=" * 70)

    print(f"\nDevice: {device}")

    if torch.cuda.is_available():

        print(
            f"GPU: "
            f"{torch.cuda.get_device_name(0)}"
        )


    # ======================================
    # Load checkpoint
    # ======================================

    print("\nLoading model...")

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=device
    )


    num_classes = checkpoint[
        "num_classes"
    ]

    class_names = checkpoint[
        "class_names"
    ]


    print(
        f"Number of classes: "
        f"{num_classes}"
    )


    # ======================================
    # Create model
    # ======================================

    model = create_model(
        num_classes=num_classes
    )

    model = model.to(device)


    # ======================================
    # Load trained weights
    # ======================================

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model.eval()


    print("\nModel loaded successfully.")


    # ======================================
    # Loss function
    # ======================================

    criterion = nn.CrossEntropyLoss()


    # ======================================
    # Testing
    # ======================================

    test_loss = 0.0

    correct = 0
    total = 0

    all_labels = []
    all_predictions = []

    top5_correct = 0


    print("\nRunning test...\n")


    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)
            labels = labels.to(device)


            # ------------------------------
            # Forward pass
            # ------------------------------

            outputs = model(images)


            # ------------------------------
            # Loss
            # ------------------------------

            loss = criterion(
                outputs,
                labels
            )

            test_loss += (
                loss.item()
                * images.size(0)
            )


            # ------------------------------
            # Top-1 prediction
            # ------------------------------

            _, predicted = torch.max(
                outputs,
                1
            )


            total += labels.size(0)

            correct += (
                predicted == labels
            ).sum().item()


            # ------------------------------
            # Top-5 prediction
            # ------------------------------

            _, top5_predictions = torch.topk(
                outputs,
                k=5,
                dim=1
            )


            for i in range(labels.size(0)):

                if labels[i] in top5_predictions[i]:

                    top5_correct += 1


            # ------------------------------
            # Store predictions
            # ------------------------------

            all_labels.extend(
                labels.cpu().numpy()
            )

            all_predictions.extend(
                predicted.cpu().numpy()
            )


    # ======================================
    # Calculate metrics
    # ======================================

    test_loss = test_loss / total

    test_accuracy = (
        correct / total
    ) * 100

    top5_accuracy = (
        top5_correct / total
    ) * 100


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


    # ======================================
    # Print overall results
    # ======================================

    print("=" * 70)
    print("TEST RESULTS")
    print("=" * 70)

    print(
        f"\nTest Loss      : "
        f"{test_loss:.4f}"
    )

    print(
        f"Test Accuracy  : "
        f"{test_accuracy:.2f}%"
    )

    print(
        f"Top-5 Accuracy : "
        f"{top5_accuracy:.2f}%"
    )

    print(
        f"Precision      : "
        f"{precision:.4f}"
    )

    print(
        f"Recall         : "
        f"{recall:.4f}"
    )

    print(
        f"F1 Score       : "
        f"{f1:.4f}"
    )


    # ======================================
    # Classification Report
    # ======================================

    print("\n")
    print("=" * 70)
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


    # ======================================
    # Final
    # ======================================

    print("=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)