#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消融实验4: ARConv-Neck — Neck的PAN下采样路径替换(Head中2个Conv)
ARConv替换层数: 2 (位置: Neck/PAN downsampling)
"""
import os
from ultralytics import YOLO
from arconv_callback import arconv_callbacks

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def main():
    model = YOLO('ultralytics/cfg/models/11/yolo11n_arconv_neck.yaml')

    arconv_count = sum(1 for m in model.model.modules() if m.__class__.__name__ == 'ARConv')
    print(f"[验证] ARConv层数: {arconv_count} (预期: 2)")

    model.train(
        data='/root/autodl-tmp/domestic_dataset/data.yaml',
        epochs=150,
        batch=16,
        imgsz=640,
        cache=True,
        close_mosaic=10,
        workers=8,
        optimizer='SGD',
        amp=True,
        device='0',
        project='runs/ablation',
        name='arconv_neck',
        exist_ok=True,
        patience=0,
        save=True,
        plots=True,
        val=True,
        callbacks=arconv_callbacks,
    )

if __name__ == '__main__':
    main()
