"""
天气图像分类 - 训练脚本（单 B0 版本，快速复现）
方案：torchvision EfficientNet-B0 预训练微调
      + 强数据增强 + 类别加权 + Label Smoothing + Cosine LR
      + 多 seed Model Soup + TTA + 阈值搜索
      + cleanlab 数据清洗（用 torchvision ResNet18 特征）
"""
import os
import sys
import json
import argparse
from pathlib import Path
from collections import Counter

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
from torchvision import transforms, datasets, models
from sklearn.metrics import f1_score, classification_report
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_predict
from sklearn.linear_model import LogisticRegression

# 确保输出不缓冲
sys.stdout.reconfigure(line_buffering=True)

LABELS = ["cloudy", "rainy", "snowy", "sunny"]
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
IMAGE_SIZE = 224


def get_train_dir():
    candidates = [
        Path("C:/Users/feiyu/Desktop/睿抗/datasets/6a39ed934d7b489daf5f80a4-momodel/train"),
        Path("/home/jovyan/work/datasets/6a39ed934d7b489daf5f80a4-momodel/train"),
        Path(__file__).resolve().parent.parent / "datasets" / "6a39ed934d7b489daf5f80a4-momodel" / "train",
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    raise FileNotFoundError("找不到训练数据集")


# ============================================================
# 第一步：数据清洗 - 用 torchvision ResNet18 特征 + cleanlab
# ============================================================
def step1_clean_data(train_dir, results_dir):
    """用 torchvision ResNet18 提取特征 + cleanlab 检测标注错误。"""
    print("\n" + "=" * 60)
    print("第一步：数据清洗（cleanlab）")
    print("=" * 60)

    image_size = IMAGE_SIZE
    tf = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])
    full_set = datasets.ImageFolder(train_dir, transform=tf)
    n = len(full_set)
    targets = np.array(full_set.targets)

    print("加载 torchvision ResNet18 提取特征 ...", flush=True)
    weights = models.ResNet18_Weights.IMAGENET1K_V1
    feat_model = models.resnet18(weights=weights)
    feat_model = nn.Sequential(*list(feat_model.children())[:-1])
    feat_model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    feat_model = feat_model.to(device)

    features = []
    batch_size = 32
    loader = DataLoader(full_set, batch_size=batch_size, shuffle=False, num_workers=0)
    with torch.no_grad():
        for i, (x, _) in enumerate(loader):
            x = x.to(device)
            feat = feat_model(x)
            feat = feat.squeeze(-1).squeeze(-1)
            features.append(feat.cpu().numpy())
            if (i + 1) % 20 == 0 or i == 0:
                print(f"  特征提取 {min((i+1)*batch_size, n)}/{n}", flush=True)
    features = np.concatenate(features, axis=0)
    print(f"特征维度: {features.shape}", flush=True)

    print("运行 cleanlab 检测标注错误 ...", flush=True)
    from cleanlab.filter import find_label_issues
    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    print("  交叉验证生成预测概率 ...", flush=True)
    pred_probs = cross_val_predict(clf, features, targets, cv=5, method="predict_proba")
    label_issues = find_label_issues(
        labels=targets,
        pred_probs=pred_probs,
        return_indices_ranked_by="self_confidence",
    )
    flagged = label_issues if isinstance(label_issues, np.ndarray) else np.array(label_issues)
    print(f"cleanlab 标记 {len(flagged)} 个潜在标注错误 / 共 {n} 个样本", flush=True)
    idx_to_class = {v: k for k, v in full_set.class_to_idx.items()}
    flagged_classes = [idx_to_class[targets[i]] for i in flagged]
    print(f"错误样本类别分布: {Counter(flagged_classes)}", flush=True)

    max_flag = int(n * 0.05)
    if len(flagged) > max_flag:
        print(f"  标记错误过多({len(flagged)})，截取置信度最高的 {max_flag} 个", flush=True)
        flagged = flagged[:max_flag]

    clean_indices = np.setdiff1d(np.arange(n), flagged)
    clean_result = {
        "total": n,
        "flagged": len(flagged),
        "flagged_indices": flagged.tolist(),
        "clean_indices": clean_indices.tolist(),
        "flagged_classes": dict(Counter(flagged_classes)),
    }
    with open(results_dir / "cleanlab_result.json", "w", encoding="utf-8") as f:
        json.dump(clean_result, f, indent=2, ensure_ascii=False)
    print(f"清洗结果保存到 {results_dir / 'cleanlab_result.json'}", flush=True)
    print(f"清洗后样本数: {len(clean_indices)}", flush=True)
    return clean_indices


# ============================================================
# 模型构建
# ============================================================
def build_model(num_classes=4):
    """构建 EfficientNet-B0 模型，加载 ImageNet 预训练权重。"""
    print("加载 torchvision EfficientNet-B0 预训练权重 ...", flush=True)
    weights = models.EfficientNet_B0_Weights.IMAGENET1K_V1
    model = models.efficientnet_b0(weights=weights)
    in_features = model.classifier[1].in_features  # 1280
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes),
    )
    print("模型加载完成", flush=True)
    return model


def get_transforms(image_size=IMAGE_SIZE):
    """训练和验证的数据增强。"""
    train_tf = transforms.Compose([
        transforms.Resize((image_size + 32, image_size + 32)),
        transforms.RandomCrop(image_size),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.15, hue=0.03),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        transforms.RandomErasing(p=0.25),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])
    return train_tf, val_tf


# ============================================================
# 第二步：训练 EfficientNet-B0（多 seed → Model Soup）
# ============================================================
def train_one_seed(train_dir, train_idx, val_idx, seed, epochs=50):
    """训练一个 seed 的 EfficientNet-B0。"""
    print(f"\n--- Seed {seed} ---", flush=True)
    torch.manual_seed(seed)
    np.random.seed(seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    image_size = IMAGE_SIZE

    train_tf, val_tf = get_transforms(image_size)
    train_set_full = datasets.ImageFolder(train_dir, transform=train_tf)
    val_set_full = datasets.ImageFolder(train_dir, transform=val_tf)
    train_set = Subset(train_set_full, train_idx)
    val_set = Subset(val_set_full, val_idx)

    train_loader = DataLoader(train_set, batch_size=16, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_set, batch_size=32, shuffle=False, num_workers=0)

    model = build_model(num_classes=len(LABELS))
    model = model.to(device)

    # 差分学习率：backbone 小学习率，分类头大学习率
    backbone_params, head_params = [], []
    for name, p in model.named_parameters():
        if "classifier" in name:
            head_params.append(p)
        else:
            backbone_params.append(p)
    optimizer = optim.AdamW([
        {"params": backbone_params, "lr": 5e-4},
        {"params": head_params, "lr": 5e-3},
    ], weight_decay=0.01)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    # 类别加权 + label smoothing
    targets = np.array(train_set_full.targets)
    train_targets = targets[train_idx]
    class_weights = compute_class_weight("balanced", classes=np.unique(train_targets), y=train_targets)
    class_weights = torch.FloatTensor(class_weights).to(device)
    print(f"类别权重: {class_weights.cpu().numpy()}", flush=True)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.1)

    best_f1 = 0
    best_state = None
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        total = 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device).long()
            optimizer.zero_grad()
            out = model(x)
            loss = criterion(out, y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * x.size(0)
            total += x.size(0)
        scheduler.step()

        # 验证
        model.eval()
        all_preds, all_targets = [], []
        with torch.no_grad():
            for x, y in val_loader:
                x = x.to(device)
                out = model(x)
                pred = out.argmax(dim=1).cpu().numpy()
                all_preds.extend(pred)
                all_targets.extend(y.numpy())
        f1 = f1_score(all_targets, all_preds, average="macro")

        if f1 > best_f1:
            best_f1 = f1
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            marker = " *"
        else:
            marker = ""

        if epoch <= 5 or epoch % 5 == 0 or epoch == epochs:
            print(f"  Epoch {epoch}/{epochs}  loss={running_loss/total:.4f}  val_f1={f1:.4f}  best={best_f1:.4f}{marker}", flush=True)

    print(f"  Seed {seed} best F1: {best_f1:.4f}", flush=True)
    return best_state, best_f1


def evaluate_model(model, val_loader, device):
    """评估模型 F1 macro。"""
    model.eval()
    all_preds, all_targets = [], []
    with torch.no_grad():
        for x, y in val_loader:
            x = x.to(device)
            out = model(x)
            pred = out.argmax(dim=1).cpu().numpy()
            all_preds.extend(pred)
            all_targets.extend(y.numpy())
    return f1_score(all_targets, all_preds, average="macro")


def search_thresholds(model, val_loader, device):
    """搜索最佳温度参数。"""
    print("\n阈值搜索 ...", flush=True)
    model.eval()
    all_logits, all_targets = [], []
    with torch.no_grad():
        for x, y in val_loader:
            x = x.to(device)
            out = model(x)
            all_logits.append(out.cpu().numpy())
            all_targets.extend(y.numpy())
    all_logits = np.concatenate(all_logits, axis=0)
    all_targets = np.array(all_targets)

    best_f1 = f1_score(all_targets, all_logits.argmax(axis=1), average="macro")
    best_temp = 1.0
    for temp in np.arange(0.5, 2.0, 0.1):
        scaled = all_logits / temp
        probs = torch.softmax(torch.from_numpy(scaled), dim=1).numpy()
        pred = probs.argmax(axis=1)
        f1 = f1_score(all_targets, pred, average="macro")
        if f1 > best_f1:
            best_f1 = f1
            best_temp = temp
    print(f"最佳温度: {best_temp:.1f}, F1: {best_f1:.4f}", flush=True)
    return {"temperature": best_temp}


def step2_train_efficientnet(train_dir, clean_indices, results_dir, n_seeds=3, epochs=50):
    """训练 EfficientNet-B0，多 seed 做 Model Soup。"""
    print("\n" + "=" * 60)
    print(f"第二步：EfficientNet-B0 微调训练（{n_seeds} seeds → Model Soup）")
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}", flush=True)
    image_size = IMAGE_SIZE
    print(f"image_size: {image_size}", flush=True)

    full_set = datasets.ImageFolder(train_dir)
    targets = np.array(full_set.targets)
    class_to_idx = full_set.class_to_idx

    # 分层划分训练/验证
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.15, random_state=42)
    train_idx, val_idx = next(sss.split(np.zeros(len(targets)), targets))

    # 清洗过滤
    if clean_indices is not None:
        clean_set = set(clean_indices.tolist())
        train_idx = np.array([i for i in train_idx if i in clean_set])
        val_idx = np.array([i for i in val_idx if i in clean_set])

    print(f"训练集: {len(train_idx)}, 验证集: {len(val_idx)}", flush=True)

    # 训练多个 seed
    all_states, all_f1s = [], []
    for seed_idx in range(n_seeds):
        seed = 42 + seed_idx * 100
        state, f1 = train_one_seed(train_dir, train_idx, val_idx, seed, epochs)
        all_states.append(state)
        all_f1s.append(f1)

    # Model Soup: 权重平均
    print("\n构建 Model Soup ...", flush=True)
    soup_state = {}
    for key in all_states[0].keys():
        soup_state[key] = sum(sd[key] for sd in all_states) / len(all_states)

    # 评估 Soup
    _, val_tf = get_transforms(image_size)
    val_set_full = datasets.ImageFolder(train_dir, transform=val_tf)
    val_set = Subset(val_set_full, val_idx)
    val_loader = DataLoader(val_set, batch_size=32, shuffle=False, num_workers=0)

    model = build_model(num_classes=len(LABELS))
    model.load_state_dict(soup_state)
    model = model.to(device)
    soup_f1 = evaluate_model(model, val_loader, device)
    print(f"Model Soup F1: {soup_f1:.4f}", flush=True)
    print(f"单模型 F1: {all_f1s}", flush=True)

    # 验证点
    if soup_f1 >= 0.90:
        print(f"[验证通过] F1 >= 0.90，效果良好！", flush=True)
    elif soup_f1 >= 0.85:
        print(f"[注意] F1 = {soup_f1:.4f}，还可以但不够好", flush=True)
    else:
        print(f"[警告] F1 = {soup_f1:.4f} < 0.85，可能有问题", flush=True)

    # 阈值搜索
    thresholds = search_thresholds(model, val_loader, device)

    # 保存
    save_dict = {
        "model_state": soup_state,
        "model_name": "efficientnet_b0",
        "labels": LABELS,
        "class_to_idx": class_to_idx,
        "image_size": image_size,
        "mean": IMAGENET_MEAN,
        "std": IMAGENET_STD,
        "val_macro_f1": soup_f1,
        "single_model_f1s": all_f1s,
        "thresholds": thresholds,
    }
    save_path = results_dir / "weather_efficientnet_b0.pth"
    torch.save(save_dict, save_path)
    print(f"保存到 {save_path}", flush=True)
    return soup_f1


# ============================================================
# 主流程
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip_clean", action="store_true", help="跳过数据清洗")
    parser.add_argument("--epochs", type=int, default=50, help="每个 seed 的训练轮数")
    parser.add_argument("--n_seeds", type=int, default=3, help="训练几个 seed 做 Model Soup")
    args = parser.parse_args()

    train_dir = get_train_dir()
    print(f"训练数据目录: {train_dir}", flush=True)

    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    print(f"结果目录: {results_dir}", flush=True)

    # 第一步：数据清洗
    clean_indices = None
    clean_path = results_dir / "cleanlab_result.json"
    if not args.skip_clean and clean_path.exists():
        with open(clean_path) as f:
            clean_indices = np.array(json.load(f)["clean_indices"])
        print(f"\n跳过清洗（已有结果），使用 {len(clean_indices)} 个样本", flush=True)
    elif not args.skip_clean:
        clean_indices = step1_clean_data(train_dir, results_dir)
    else:
        print("\n跳过数据清洗", flush=True)

    # 第二步：训练 EfficientNet-B0
    f1 = step2_train_efficientnet(
        train_dir, clean_indices, results_dir,
        n_seeds=args.n_seeds, epochs=args.epochs
    )

    print("\n" + "=" * 60)
    print("训练完成！", flush=True)
    print(f"EfficientNet-B0 Model Soup F1: {f1:.4f}", flush=True)
    print("=" * 60)
    print("接下来运行 main.py 进行推理验证", flush=True)


if __name__ == "__main__":
    main()
