import torch
import torch.nn as nn

from torchvision.models import (
    efficientnet_b0,
    EfficientNet_B0_Weights
)


# ==========================================
# Configuration
# ==========================================

NUM_CLASSES = 66


# ==========================================
# Create EfficientNet-B0
# ==========================================

def create_model(num_classes=NUM_CLASSES):

    # Load pretrained EfficientNet-B0
    weights = EfficientNet_B0_Weights.DEFAULT

    model = efficientnet_b0(weights=weights)


    # --------------------------------------
    # Freeze pretrained layers
    # --------------------------------------

    for parameter in model.features.parameters():

        parameter.requires_grad = False


    # --------------------------------------
    # Replace classifier
    # --------------------------------------

    input_features = model.classifier[1].in_features

    model.classifier[1] = nn.Linear(
        input_features,
        num_classes
    )


    return model


# ==========================================
# Test model
# ==========================================

if __name__ == "__main__":

    print("=" * 60)
    print("EFFICIENTNET-B0 MODEL TEST")
    print("=" * 60)


    # Create model
    model = create_model()


    # Print classifier
    print("\nClassifier:")
    print(model.classifier)


    # Count parameters
    total_parameters = sum(
        parameter.numel()
        for parameter in model.parameters()
    )

    trainable_parameters = sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )


    print(f"\nTotal parameters     : {total_parameters:,}")
    print(f"Trainable parameters : {trainable_parameters:,}")


    # Test input
    test_input = torch.randn(
        2,
        3,
        224,
        224
    )


    # Forward pass
    with torch.no_grad():

        output = model(test_input)


    print("\nInput shape:")
    print(test_input.shape)


    print("\nOutput shape:")
    print(output.shape)


    print("\nExpected output:")
    print("(batch_size, 66)")


    if output.shape == (2, 66):

        print("\nMODEL TEST PASSED")

    else:

        print("\nMODEL TEST FAILED")


    print("\n" + "=" * 60)