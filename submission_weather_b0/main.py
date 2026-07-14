"""
天气图像分类 - 推理脚本
EfficientNet-B0 + TTA + 温度缩放
"""
import os
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

LABELS = ["cloudy", "rainy", "snowy", "sunny"]
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

try:
    RESAMPLE_BILINEAR = Image.Resampling.BILINEAR
except AttributeError:
    RESAMPLE_BILINEAR = Image.BILINEAR


# ============================================================
# 模型构建与加载
# ============================================================
def build_model(num_classes=4):
    """构建 EfficientNet-B0 模型结构（不含预训练权重）。"""
    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features  # 1280
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes),
    )
    return model


def load_model(checkpoint_path):
    """加载训练好的模型。"""
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    num_classes = len(checkpoint.get("labels", LABELS))
    model = build_model(num_classes=num_classes)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    model = model.to(device)
    return {
        "model": model,
        "image_size": checkpoint.get("image_size", 224),
        "thresholds": checkpoint.get("thresholds", {"temperature": 1.0}),
        "labels": checkpoint.get("labels", LABELS),
        "val_f1": checkpoint.get("val_macro_f1", 0),
    }


# 加载模型
MODEL_BUNDLE = None
checkpoint_path = PROJECT_ROOT / "results" / "weather_efficientnet_b0.pth"
if checkpoint_path.exists():
    print(f"加载模型: {checkpoint_path}")
    MODEL_BUNDLE = load_model(checkpoint_path)
    print(f"  val_f1={MODEL_BUNDLE['val_f1']:.4f}")
else:
    raise FileNotFoundError(
        f"找不到模型权重: {checkpoint_path}\n请先运行 train_final.py 训练模型。"
    )


# ============================================================
# 图像预处理
# ============================================================
def _to_rgb(X):
    """cv2 BGR -> RGB。"""
    if X is None:
        raise ValueError("predict() received None")
    if X.ndim == 2:
        X = cv2.cvtColor(X, cv2.COLOR_GRAY2BGR)
    if X.ndim != 3 or X.shape[2] not in (3, 4):
        raise ValueError(f"Unexpected image shape: {X.shape}")
    if X.shape[2] == 4:
        X = X[:, :, :3]
    return cv2.cvtColor(X, cv2.COLOR_BGR2RGB)


def _preprocess_image(rgb, image_size):
    """RGB -> normalized tensor (1, 3, H, W)。"""
    image = Image.fromarray(rgb).resize((image_size, image_size), RESAMPLE_BILINEAR)
    image = np.asarray(image, dtype=np.float32) / 255.0
    image = (image - np.array(IMAGENET_MEAN, dtype=np.float32)) / np.array(IMAGENET_STD, dtype=np.float32)
    image = np.transpose(image, (2, 0, 1))[np.newaxis, :, :, :]
    return torch.from_numpy(image).to(device)


def _get_tta_images(rgb, image_size):
    """生成 TTA 增强图像列表：原图 + 水平翻转。"""
    images = []
    images.append(_preprocess_image(rgb, image_size))
    rgb_flip = rgb[:, ::-1, :].copy()
    images.append(_preprocess_image(rgb_flip, image_size))
    return images


# ============================================================
# 推理
# ============================================================
@torch.no_grad()
def predict(X):
    """
    模型预测

    param:
        X : np.ndarray，由 cv2.imread 读取的图片数据，shape(224,224,3)。
    return:
        y_predict : str, 天气类别标签，取值为 'sunny', 'cloudy', 'rainy', 'snowy' 之一。
    """
    rgb = _to_rgb(X)
    image_size = MODEL_BUNDLE["image_size"]
    temperature = MODEL_BUNDLE["thresholds"].get("temperature", 1.0)

    # TTA: 原图 + 水平翻转，取平均 logits
    tta_images = _get_tta_images(rgb, image_size)
    tta_logits = None
    for img_tensor in tta_images:
        logits = MODEL_BUNDLE["model"](img_tensor)
        tta_logits = logits if tta_logits is None else tta_logits + logits
    tta_logits = tta_logits / len(tta_images)

    # 温度缩放
    if temperature != 1.0:
        tta_logits = tta_logits / temperature

    pred_idx = int(torch.argmax(tta_logits, dim=1).item())
    return LABELS[pred_idx]


# ============================================================
# 本地测试
# ============================================================
if __name__ == "__main__":
    from sklearn.metrics import f1_score, classification_report

    train_dir = PROJECT_ROOT.parent / "datasets" / "6a39ed934d7b489daf5f80a4-momodel" / "train"

    if not train_dir.exists():
        print("找不到训练数据目录，跳过测试")
        exit()

    print("\n本地测试 ...")
    all_preds, all_targets = [], []

    for label_name in LABELS:
        label_dir = train_dir / label_name
        files = sorted(label_dir.glob("*.jpg"))
        np.random.seed(42)
        test_files = np.random.choice(files, min(20, len(files)), replace=False)
        for f in test_files:
            img = cv2.imread(str(f))
            if img is None:
                continue
            pred = predict(img)
            all_preds.append(pred)
            all_targets.append(label_name)
            if len(all_preds) % 10 == 0:
                print(f"  {len(all_preds)}/80 测试完成")

    print(f"\n测试样本数: {len(all_preds)}")
    print(f"F1 macro: {f1_score(all_targets, all_preds, average='macro'):.4f}")
    print("\n分类报告:")
    print(classification_report(all_targets, all_preds, target_names=LABELS))
