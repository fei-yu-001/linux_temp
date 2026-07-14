#!/usr/bin/env python3
"""
ARConv Full 稳定训练脚本 - 降低学习率版本
解决梯度爆炸问题
"""

from ultralytics import YOLO
from arconv_callback import arconv_callbacks
import os

# 解决OpenMP库冲突
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 优化PyTorch性能
os.environ['CUDA_LAUNCH_BLOCKING'] = '0'
os.environ['TORCH_CUDNN_V8_API_ENABLED'] = '1'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
os.environ['OMP_NUM_THREADS'] = '12'
os.environ['MKL_NUM_THREADS'] = '12'

print("="*80)
print("  ARConv Full 稳定训练 - 降低学习率版本")
print("="*80)
print()
print("修改内容：")
print("  1. 学习率: 0.01 → 0.005 (降低50%，防止梯度爆炸)")
print("  2. 优化器: SGD")
print("  3. Momentum: 0.9")
print()

# 加载模型
model = YOLO('ultralytics/cfg/models/11/yolo11n_arconv_full.yaml')

# 添加ARConv回调
for event, callback in arconv_callbacks.items():
    model.add_callback(event, callback)

print("✅ 已添加ARConv回调")
print()

# 训练参数 - 降低学习率
train_params = {
    'data': 'domestic_dataset/data.yaml',
    'epochs': 150,
    'batch': 48,
    'imgsz': 640,
    'device': '0',
    'workers': 12,
    'cache': True,
    'amp': True,
    'half': False,
    'mosaic': False,
    'close_mosaic': 0,
    'project': 'runs/ablation',
    'name': 'arconv_full',
    'patience': 50,
    'save': True,
    'save_period': 15,
    'val': True,
    'plots': True,
    'verbose': True,
    'deterministic': False,
    'rect': False,
    # 关键修改：降低学习率
    'optimizer': 'SGD',
    'lr0': 0.005,  # 初始学习率从0.01降到0.005
    'lrf': 0.01,   # 最终学习率
    'momentum': 0.9,
    'weight_decay': 0.0005,
}

print("🚀 开始训练 arconv_full (稳定版)...")
print(f"配置: lr0={train_params['lr0']}, batch={train_params['batch']}, workers={train_params['workers']}")
print()

# 开始训练
results = model.train(**train_params)

print()
print("="*80)
print("✅ 训练完成！")
print("="*80)
