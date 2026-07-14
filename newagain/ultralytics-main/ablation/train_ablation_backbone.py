#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消融实验5: ARConv-Backbone — Backbone全部5个下采样Conv替换
ARConv替换层数: 5
"""
import os
from ultralytics import YOLO
from arconv_callback import arconv_callbacks

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def main():
    model = YOLO('ultralytics/cfg/models/11/yolo11n_arconv_backbone.yaml')

    arconv_count = sum(1 for m in model.model.modules() if m.__class__.__name__ == 'ARConv')
    print(f"[验证] ARConv层数: {arconv_count} (预期: 5)")

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
        name='arconv_backbone',
        exist_ok=True,
        patience=0,
        save=True,
        plots=True,
        val=True,
        callbacks=arconv_callbacks,
    )

if __name__ == '__main__':
    main()
