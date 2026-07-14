#!/usr/bin/env python3
"""
YOLOv11n Baseline Training Script - 消融实验基线
训练原版YOLOv11n模型（不使用ARConv）
"""

import os
from ultralytics import YOLO

# 解决OpenMP库冲突问题（参考CSDN教程）
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def main():
    # 加载模型配置
    model = YOLO(model='ultralytics/cfg/models/11/yolo11n_baseline.yaml')
    
    # 训练参数
    results = model.train(
        data='/root/autodl-tmp/domestic_dataset/data.yaml',  # 数据集配置文件
        epochs=150,                    # 训练轮数
        batch=16,                      # 批次大小
        imgsz=640,                     # 图像大小
        device='0',                    # GPU设备
        workers=4,                     # 数据加载线程数
        cache=True,                    # 缓存数据集
        amp=True,                      # 自动混合精度
        mosaic=True,                   # Mosaic数据增强
        project='runs/ablation',       # 项目目录
        name='baseline',               # 实验名称
        exist_ok=True,                 # 允许覆盖
        patience=50,                   # 早停耐心值
        save=True,                     # 保存检查点
        plots=True,                    # 生成图表
        val=True,                      # 验证
    )
    
    print("\n" + "="*50)
    print("训练完成！")
    print(f"最佳模型保存在: runs/ablation/baseline/weights/best.pt")
    print("="*50)

if __name__ == '__main__':
    main()
