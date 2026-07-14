#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消融实验6: ARConv-Full — Backbone×5 + Head×2 全部替换
ARConv替换层数: 7
"""
import os
from ultralytics import YOLO
from arconv_callback import arconv_callbacks

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def main():
    model = YOLO('ultralytics/cfg/models/11/yolo11n_arconv_full.yaml')

    arconv_count = sum(1 for m in model.model.modules() if m.__class__.__name__ == 'ARConv')
    print(f"[验证] ARConv层数: {arconv_count} (预期: 7)")

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
        name='arconv_full',
        exist_ok=True,
        patience=0,
        save=True,
        plots=True,
        val=True,
        callbacks=arconv_callbacks,
    )

if __name__ == '__main__':
    main()
