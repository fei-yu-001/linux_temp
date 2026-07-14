#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量运行YOLO模型对比实验
训练模型：YOLOv8, YOLO11, YOLO12, YOLOv10 + YOLO11(ARConv minimal)
"""
import subprocess
import time
from datetime import datetime

def run_training(script_name, model_name):
    """运行单个训练脚本"""
    print(f"\n{'='*60}")
    print(f"开始训练 {model_name}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    try:
        # 运行训练脚本
        result = subprocess.run(
            ['python', script_name],
            check=True,
            capture_output=False
        )
        
        elapsed_time = time.time() - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        
        print(f"\n✓ {model_name} 训练完成！")
        print(f"用时: {hours}小时{minutes}分钟")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {model_name} 训练失败！")
        print(f"错误: {e}")
        return False

def main():
    """主函数：依次训练所有模型"""
    experiments = [
        ('train_yolov8_domestic.py', 'YOLOv8n'),
        ('train_yolo11_domestic.py', 'YOLO11n'),
        ('train_yolo12_domestic.py', 'YOLO12n'),
        ('train_yolov10_domestic.py', 'YOLOv10n'),
        ('train_yolo11_arconv_minimal_domestic.py', 'YOLO11n + ARConv(minimal)'),
    ]
    
    print("="*60)
    print("YOLO模型对比实验")
    print("="*60)
    print(f"数据集: domestic_dataset (31类昆虫)")
    print(f"训练参数: epochs=150, batch=16, imgsz=640")
    print(f"模型数量: {len(experiments)}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    start_time = time.time()
    results = {}
    
    # 依次训练每个模型
    for script, model_name in experiments:
        success = run_training(script, model_name)
        results[model_name] = success
        
        if not success:
            print(f"\n警告: {model_name} 训练失败，继续下一个模型...")
    
    # 打印总结
    total_time = time.time() - start_time
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    
    print("\n" + "="*60)
    print("实验完成总结")
    print("="*60)
    print(f"总用时: {hours}小时{minutes}分钟")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n训练结果:")
    for model_name, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        print(f"  {model_name}: {status}")
    
    print("\n模型保存位置:")
    print("  runs/train/yolov8n_domestic/weights/best.pt")
    print("  runs/train/yolo11n_domestic/weights/best.pt")
    print("  runs/train/yolo12n_domestic/weights/best.pt")
    print("  runs/train/yolov10n_domestic/weights/best.pt")
    print("  runs/train/yolo11n_arconv_minimal_domestic/weights/best.pt")
    print("="*60)

if __name__ == '__main__':
    main()
