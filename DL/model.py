import torch
import torch.nn as nn

from torchvision.models import (
    convnext_tiny,
    ConvNeXt_Tiny_Weights
)


NUM_CLASSES = 60


def create_model(num_classes=NUM_CLASSES):

    weights = ConvNeXt_Tiny_Weights.DEFAULT

    model = convnext_tiny(
        weights=weights
    )

    # Freeze entire pretrained model
    for parameter in model.parameters():
        parameter.requires_grad = False

    # Unfreeze final feature stage
    for parameter in model.features[-1].parameters():
        parameter.requires_grad = True

    # Replace classifier
    input_features = model.classifier[-1].in_features

    model.classifier[-1] = nn.Linear(
        input_features,
        num_classes
    )

    return model


if __name__ == "__main__":

    model = create_model()

    print(model)

    total_parameters = sum(
        p.numel()
        for p in model.parameters()
    )

    trainable_parameters = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    print("\nTotal parameters     :", f"{total_parameters:,}")
    print("Trainable parameters :", f"{trainable_parameters:,}")

    x = torch.randn(
        2,
        3,
        224,
        224
    )

    with torch.no_grad():
        output = model(x)

    print("\nInput :", x.shape)
    print("Output:", output.shape)

    if output.shape == (2, NUM_CLASSES):
        print("\nMODEL TEST PASSED")