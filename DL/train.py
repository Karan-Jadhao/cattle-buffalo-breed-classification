import os
import json
import copy

import torch
import torch.nn as nn
import torch.optim as optim

from dataset import train_loader, val_loader
from model import create_model


NUM_CLASSES = 60
NUM_EPOCHS = 40
LEARNING_RATE = 0.0001
WEIGHT_DECAY = 0.0001
PATIENCE = 5

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "efficientnet_b0_cattle_breed_model.pth"
)


def main():

    # ==========================================
    # Device
    # ==========================================

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("=" * 70)
    print("CATTLE & BUFFALO BREED CLASSIFICATION")
    print("=" * 70)

    print(f"\nDevice: {device}")

    if torch.cuda.is_available():
        print(
            f"GPU: {torch.cuda.get_device_name(0)}"
        )


    # ==========================================
    # Create model
    # ==========================================

    model = create_model(
        num_classes=NUM_CLASSES
    )

    model = model.to(device)


    # ==========================================
    # Loss
    # ==========================================

    criterion = nn.CrossEntropyLoss()


    # ==========================================
    # Optimizer
    # ==========================================

    optimizer = optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY
    )


    # ==========================================
    # Scheduler
    # ==========================================

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.5,
        patience=2
    )


    # ==========================================
    # Create directories
    # ==========================================

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )


    # ==========================================
    # Training variables
    # ==========================================

    best_val_accuracy = 0.0

    best_model_weights = copy.deepcopy(
        model.state_dict()
    )

    epochs_without_improvement = 0


    history = {
        "train_loss": [],
        "train_accuracy": [],
        "val_loss": [],
        "val_accuracy": []
    }


    # ==========================================
    # Training
    # ==========================================

    for epoch in range(NUM_EPOCHS):

        print("\n" + "=" * 70)
        print(
            f"Epoch {epoch + 1}/{NUM_EPOCHS}"
        )
        print("=" * 70)


        # ======================================
        # Training
        # ======================================

        model.train()

        running_loss = 0.0
        correct = 0
        total = 0


        for images, labels in train_loader:

            images = images.to(
                device,
                non_blocking=True
            )

            labels = labels.to(
                device,
                non_blocking=True
            )


            optimizer.zero_grad(
                set_to_none=True
            )


            outputs = model(images)


            loss = criterion(
                outputs,
                labels
            )


            loss.backward()

            optimizer.step()


            running_loss += (
                loss.item() *
                images.size(0)
            )


            predicted = outputs.argmax(
                dim=1
            )


            total += labels.size(0)

            correct += (
                predicted == labels
            ).sum().item()


        train_loss = (
            running_loss / total
        )

        train_accuracy = (
            correct / total
        ) * 100


        # ======================================
        # Validation
        # ======================================

        model.eval()

        val_running_loss = 0.0
        val_correct = 0
        val_total = 0


        with torch.no_grad():

            for images, labels in val_loader:

                images = images.to(
                    device,
                    non_blocking=True
                )

                labels = labels.to(
                    device,
                    non_blocking=True
                )


                outputs = model(images)


                loss = criterion(
                    outputs,
                    labels
                )


                val_running_loss += (
                    loss.item() *
                    images.size(0)
                )


                predicted = outputs.argmax(
                    dim=1
                )


                val_total += labels.size(0)

                val_correct += (
                    predicted == labels
                ).sum().item()


        val_loss = (
            val_running_loss /
            val_total
        )

        val_accuracy = (
            val_correct /
            val_total
        ) * 100


        # ======================================
        # Scheduler
        # ======================================

        scheduler.step(val_loss)


        # ======================================
        # Save history
        # ======================================

        history["train_loss"].append(
            train_loss
        )

        history["train_accuracy"].append(
            train_accuracy
        )

        history["val_loss"].append(
            val_loss
        )

        history["val_accuracy"].append(
            val_accuracy
        )


        # ======================================
        # Print
        # ======================================

        current_lr = (
            optimizer.param_groups[0]["lr"]
        )


        print(
            f"\nTrain Loss     : {train_loss:.4f}"
        )

        print(
            f"Train Accuracy : {train_accuracy:.2f}%"
        )

        print(
            f"Val Loss       : {val_loss:.4f}"
        )

        print(
            f"Val Accuracy   : {val_accuracy:.2f}%"
        )

        print(
            f"Learning Rate  : {current_lr:.7f}"
        )


        # ======================================
        # Save best model
        # ======================================

        if val_accuracy > best_val_accuracy:

            best_val_accuracy = val_accuracy

            best_model_weights = copy.deepcopy(
                model.state_dict()
            )

            epochs_without_improvement = 0


            # Get class names
            class_names = (
                train_loader.dataset.data["breed"]
                .unique()
                .tolist()
            )

            class_names = sorted(
                class_names
            )


            checkpoint = {

                "model_state_dict":
                    best_model_weights,

                "num_classes":
                    NUM_CLASSES,

                "class_names":
                    class_names,

                "image_size":
                    224,

                "best_val_accuracy":
                    best_val_accuracy
            }


            torch.save(
                checkpoint,
                MODEL_PATH
            )


            print(
                "\n✓ Best model saved!"
            )

            print(
                f"  Validation Accuracy: "
                f"{best_val_accuracy:.2f}%"
            )


        else:

            epochs_without_improvement += 1


        # ======================================
        # Early stopping
        # ======================================

        if (
            epochs_without_improvement
            >= PATIENCE
        ):

            print(
                "\nEarly stopping triggered."
            )

            break


    # ==========================================
    # Restore best model
    # ==========================================

    model.load_state_dict(
        best_model_weights
    )


    # ==========================================
    # Save history
    # ==========================================

    os.makedirs(
        "results",
        exist_ok=True
    )


    with open(
        "results/training_history.json",
        "w"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


    # ==========================================
    # Final information
    # ==========================================

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)

    print(
        f"\nBest Validation Accuracy: "
        f"{best_val_accuracy:.2f}%"
    )

    print(
        f"Model saved at: "
        f"{MODEL_PATH}"
    )

    print(
        "\nTraining history saved at:"
        " results/training_history.json"
    )

    print("=" * 70)


# ==========================================
# IMPORTANT FOR WINDOWS
# ==========================================

if __name__ == "__main__":

    main()