#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO模型训练结果对比分析脚本
分析YOLOv8n, YOLO11n, YOLOv9c, YOLOv10n的训练结果
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 定义模型列表
models = {
    'YOLOv8n': 'download_results/yolov8n_results.csv',
    'YOLO11n': 'download_results/yolo11n_results.csv',
    'YOLOv9c': 'download_results/yolov9c_results.csv',
    'YOLOv10n': 'download_results/yolov10n_results.csv'
}

# 读取所有结果
results = {}
for model_name, csv_path in models.items():
    if os.path.exists(csv_path):
        results[model_name] = pd.read_csv(csv_path)
        print(f"✓ 成功读取 {model_name} 的结果")
    else:
        print(f"✗ 未找到 {model_name} 的结果文件: {csv_path}")

print(f"\n共读取 {len(results)} 个模型的训练结果\n")

# 提取最终性能指标（最后一个epoch）
print("=" * 80)
print("最终性能对比 (Epoch 150)")
print("=" * 80)
print(f"{'模型':<12} {'mAP50':<10} {'mAP50-95':<12} {'Precision':<12} {'Recall':<10}")
print("-" * 80)

final_metrics = {}
for model_name, df in results.items():
    last_row = df.iloc[-1]
    final_metrics[model_name] = {
        'mAP50': last_row['metrics/mAP50(B)'],
        'mAP50-95': last_row['metrics/mAP50-95(B)'],
        'Precision': last_row['metrics/precision(B)'],
        'Recall': last_row['metrics/recall(B)']
    }
    print(f"{model_name:<12} {final_metrics[model_name]['mAP50']:<10.4f} "
          f"{final_metrics[model_name]['mAP50-95']:<12.4f} "
          f"{final_metrics[model_name]['Precision']:<12.4f} "
          f"{final_metrics[model_name]['Recall']:<10.4f}")

# 找出最佳模型
best_map50 = max(final_metrics.items(), key=lambda x: x[1]['mAP50'])
best_map50_95 = max(final_metrics.items(), key=lambda x: x[1]['mAP50-95'])

print("\n" + "=" * 80)
print("最佳模型")
print("=" * 80)
print(f"mAP50 最高: {best_map50[0]} ({best_map50[1]['mAP50']:.4f})")
print(f"mAP50-95 最高: {best_map50_95[0]} ({best_map50_95[1]['mAP50-95']:.4f})")

# 绘制训练曲线对比图
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('YOLO模型训练结果对比 (31类昆虫检测)', fontsize=16, fontweight='bold')

# mAP50曲线
ax = axes[0, 0]
for model_name, df in results.items():
    ax.plot(df['epoch'], df['metrics/mAP50(B)'], label=model_name, linewidth=2)
ax.set_xlabel('Epoch')
ax.set_ylabel('mAP50')
ax.set_title('mAP@0.5 对比')
ax.legend()
ax.grid(True, alpha=0.3)

# mAP50-95曲线
ax = axes[0, 1]
for model_name, df in results.items():
    ax.plot(df['epoch'], df['metrics/mAP50-95(B)'], label=model_name, linewidth=2)
ax.set_xlabel('Epoch')
ax.set_ylabel('mAP50-95')
ax.set_title('mAP@0.5:0.95 对比')
ax.legend()
ax.grid(True, alpha=0.3)

# Precision曲线
ax = axes[1, 0]
for model_name, df in results.items():
    ax.plot(df['epoch'], df['metrics/precision(B)'], label=model_name, linewidth=2)
ax.set_xlabel('Epoch')
ax.set_ylabel('Precision')
ax.set_title('Precision 对比')
ax.legend()
ax.grid(True, alpha=0.3)

# Recall曲线
ax = axes[1, 1]
for model_name, df in results.items():
    ax.plot(df['epoch'], df['metrics/recall(B)'], label=model_name, linewidth=2)
ax.set_xlabel('Epoch')
ax.set_ylabel('Recall')
ax.set_title('Recall 对比')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
print(f"\n✓ 对比图已保存到: model_comparison.png")

# 绘制Loss曲线对比
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('训练Loss对比', fontsize=16, fontweight='bold')

# Box Loss
ax = axes[0]
for model_name, df in results.items():
    ax.plot(df['epoch'], df['train/box_loss'], label=model_name, linewidth=2)
ax.set_xlabel('Epoch')
ax.set_ylabel('Box Loss')
ax.set_title('Box Loss')
ax.legend()
ax.grid(True, alpha=0.3)

# Class Loss
ax = axes[1]
for model_name, df in results.items():
    ax.plot(df['epoch'], df['train/cls_loss'], label=model_name, linewidth=2)
ax.set_xlabel('Epoch')
ax.set_ylabel('Class Loss')
ax.set_title('Classification Loss')
ax.legend()
ax.grid(True, alpha=0.3)

# DFL Loss
ax = axes[2]
for model_name, df in results.items():
    ax.plot(df['epoch'], df['train/dfl_loss'], label=model_name, linewidth=2)
ax.set_xlabel('Epoch')
ax.set_ylabel('DFL Loss')
ax.set_title('DFL Loss')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('loss_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Loss对比图已保存到: loss_comparison.png")

print("\n" + "=" * 80)
print("分析完成！")
print("=" * 80)
