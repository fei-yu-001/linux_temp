#!/usr/bin/env python3
"""
YOLOv11n + ARConv Full Training Script - 消融实验完整版
在Backbone和Head中全部使用ARConv
"""

from ultralytics import YOLO
from arconv_callback import arconv_callbacks

def main():
    # 加载模型配置
    model = YOLO('ultralytics/cfg/models/11/yolo11n_arconv_full.yaml')
    
    # 训练参数
    results = model.train(
        data='/root/autodl-tmp/domestic_dataset/data.yaml',  # 数据集配置文件
        epochs=150,                    # 训练轮数
        batch=16,                      # 批次大小
        imgsz=640,                     # 图像大小
        cache=True,                    # 缓存数据集
        device=0,                      # GPU设备
        project='runs/ablation',       # 项目目录
        name='arconv_full',            # 实验名称
        exist_ok=True,                 # 允许覆盖
        amp=True,                      # 自动混合精度
        patience=50,                   # 早停耐心值
        save=True,                     # 保存检查点
        plots=True,                    # 生成图表
        val=True,                      # 验证
        callbacks=arconv_callbacks,    # ARConv回调（更新epoch）
    )
    
    print("\n" + "="*50)
    print("训练完成！")
    print(f"最佳模型保存在: runs/ablation/arconv_full/weights/best.pt")
    print("="*50)

if __name__ == '__main__':
    main()
