#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ultralytics import YOLO

# 加载YOLOv10模型
model = YOLO('yolov10n.yaml')

# 训练模型
results = model.train(
    data='/root/autodl-tmp/domestic_dataset/data.yaml',
    epochs=150,
    batch=16,
    imgsz=640,
    cache=True,
    close_mosaic=10,
    workers=8,
    device='0',
    optimizer='SGD',
    amp=True,
    project='runs/train',
    name='yolov10n_domestic'
)

print("YOLOv10训练完成！")
print(f"最佳模型保存在: {results.save_dir}")
