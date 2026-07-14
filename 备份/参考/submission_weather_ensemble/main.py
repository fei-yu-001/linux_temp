from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models


try:
    PROJECT_ROOT = Path(__file__).resolve().parent
except NameError:
    PROJECT_ROOT = Path.cwd()
MODEL_SPECS = [
    (PROJECT_ROOT / "results" / "weather_efficientnet_b2_best.pth", 0.4),
    (PROJECT_ROOT / "results" / "weather_efficientnet_b0_best.pth", 0.6),
]
LABELS = ["cloudy", "rainy", "snowy", "sunny"]
IM_SIZE = 224
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
try:
    RESAMPLE_BILINEAR = Image.Resampling.BILINEAR
except AttributeError:
    RESAMPLE_BILINEAR = Image.BILINEAR


def build_model(model_name, num_classes):
    if model_name == "resnet18":
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
    elif model_name == "resnet50":
        model = models.resnet50(weights=None)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
    elif model_name == "efficientnet_b0":
        model = models.efficientnet_b0(weights=None)
        in_features = model.classifier[-1].in_features
        model.classifier[-1] = nn.Linear(in_features, num_classes)
    elif model_name == "efficientnet_b2":
        model = models.efficientnet_b2(weights=None)
        in_features = model.classifier[-1].in_features
        model.classifier[-1] = nn.Linear(in_features, num_classes)
    elif model_name == "mobilenet_v3_large":
        model = models.mobilenet_v3_large(weights=None)
        in_features = model.classifier[-1].in_features
        model.classifier[-1] = nn.Linear(in_features, num_classes)
    else:
        raise ValueError(f"Unsupported model: {model_name}")
    return model


def load_checkpoint(path):
    if not path.exists():
        raise FileNotFoundError(f"Model checkpoint not found: {path}")
    try:
        return torch.load(path, map_location=device, weights_only=False)
    except TypeError:
        return torch.load(path, map_location=device)


def build_inference_bundle(path, weight):
    checkpoint = load_checkpoint(path)
    model_name = checkpoint.get("model_name", "resnet18") if isinstance(checkpoint, dict) else "resnet18"
    labels = checkpoint.get("labels", LABELS) if isinstance(checkpoint, dict) else LABELS
    image_size = int(checkpoint.get("image_size", IM_SIZE)) if isinstance(checkpoint, dict) else IM_SIZE
    mean = np.array(checkpoint.get("mean", MEAN), dtype=np.float32) if isinstance(checkpoint, dict) else MEAN
    std = np.array(checkpoint.get("std", STD), dtype=np.float32) if isinstance(checkpoint, dict) else STD

    inference_model = build_model(model_name, len(labels)).to(device)
    state_dict = (
        checkpoint["model_state"]
        if isinstance(checkpoint, dict) and "model_state" in checkpoint
        else checkpoint
    )
    inference_model.load_state_dict(state_dict)
    inference_model.eval()
    return {
        "path": path,
        "weight": float(weight),
        "model_name": model_name,
        "labels": list(labels),
        "image_size": image_size,
        "mean": mean,
        "std": std,
        "model": inference_model,
    }


MODEL_BUNDLES = []
for model_path, model_weight in MODEL_SPECS:
    bundle = build_inference_bundle(model_path, model_weight)
    if not MODEL_BUNDLES:
        LABELS = bundle["labels"]
        IM_SIZE = bundle["image_size"]
        MEAN = bundle["mean"]
        STD = bundle["std"]
    elif bundle["labels"] != LABELS:
        raise ValueError(f"Label mismatch in checkpoint: {bundle['path']}")
    MODEL_BUNDLES.append(bundle)

MODEL_PATH = MODEL_BUNDLES[0]["path"]
MODEL_NAME = MODEL_BUNDLES[0]["model_name"]
model = MODEL_BUNDLES[0]["model"]


def _to_rgb(X):
    if X is None:
        raise ValueError("predict() received None")
    if X.ndim == 2:
        X = cv2.cvtColor(X, cv2.COLOR_GRAY2BGR)
    if X.ndim != 3 or X.shape[2] not in (3, 4):
        raise ValueError(f"Unexpected image shape: {X.shape}")
    if X.shape[2] == 4:
        X = X[:, :, :3]
    return cv2.cvtColor(X, cv2.COLOR_BGR2RGB)


def _preprocess_rgb(rgb, image_size, mean, std):
    image = Image.fromarray(rgb).resize((image_size, image_size), RESAMPLE_BILINEAR)
    image = np.asarray(image)
    image = image.astype(np.float32) / 255.0
    image = (image - mean) / std
    image = np.transpose(image, (2, 0, 1))[np.newaxis, :, :, :]
    return torch.from_numpy(image).to(device)


def preprocess(X):
    return _preprocess_rgb(_to_rgb(X), IM_SIZE, MEAN, STD)


def predict(X):
    """
    Predict one weather label from an image loaded by cv2.imread.

    Args:
        X: np.ndarray, BGR image with shape (H, W, 3), usually (224, 224, 3).

    Returns:
        One of: "sunny", "cloudy", "rainy", "snowy".
    """
    rgb = _to_rgb(X)
    with torch.no_grad():
        logits = None
        for bundle in MODEL_BUNDLES:
            tensor = _preprocess_rgb(
                rgb, bundle["image_size"], bundle["mean"], bundle["std"]
            )
            weighted_logits = bundle["model"](tensor) * bundle["weight"]
            logits = weighted_logits if logits is None else logits + weighted_logits
    return LABELS[int(torch.argmax(logits, dim=1).item())]
