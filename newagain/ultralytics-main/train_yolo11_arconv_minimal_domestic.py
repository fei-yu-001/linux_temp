#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from ultralytics import YOLO
from arconv_callback import arconv_callbacks

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 加载YOLO11n + ARConv(最小替换)模型
model = YOLO('ultralytics/cfg/models/11/yolo11n_arconv_minimal.yaml')

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
    name='yolo11n_arconv_minimal_domestic',
    callbacks=arconv_callbacks,
)

print('YOLO11n+ARConv(minimal)训练完成！')
print(f'最佳模型保存在: {results.save_dir}')
