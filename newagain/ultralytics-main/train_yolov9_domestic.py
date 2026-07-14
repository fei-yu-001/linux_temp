#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ultralytics import YOLO

# 加载YOLOv9模型
model = YOLO('yolov9c.yaml')

# 训练模型
results = model.train(
    data='/root/autodl-tmp/domestic_dataset/data.yaml',
    epochs=150,
    batch=16,
    imgsz=640,
    cache=True,
    device=0,
    amp=True,
    project='runs/train',
    name='yolov9c_domestic'
)

print("YOLOv9训练完成！")
print(f"最佳模型保存在: {results.save_dir}")
