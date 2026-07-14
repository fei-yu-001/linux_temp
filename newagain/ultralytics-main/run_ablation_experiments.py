#!/usr/bin/env python3
"""
ARConv消融实验批量运行脚本
按顺序运行所有5个消融实验
"""

import subprocess
import sys
import time
from datetime import datetime

def run_experiment(script_name, experiment_name):
    """运行单个实验"""
    print("\n" + "="*70)
    print(f"开始实验: {experiment_name}")
    print(f"脚本: {script_name}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    start_time = time.time()
    
    try:
        # 运行训练脚本
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        
        elapsed_time = time.time() - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        
        print("\n" + "="*70)
        print(f"✓ 实验完成: {experiment_name}")
        print(f"耗时: {hours}小时 {minutes}分钟")
        print("="*70 + "\n")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "="*70)
        print(f"✗ 实验失败: {experiment_name}")
        print(f"错误: {e}")
        print("="*70 + "\n")
        return False

def main():
    """主函数：按顺序运行所有消融实验"""
    
    experiments = [
        ("train_ablation_baseline.py", "基线 - 原版YOLOv11n"),
        ("train_ablation_backbone.py", "消融1 - Backbone ARConv"),
        ("train_ablation_neck.py", "消融2 - Neck Fusion ARConv"),
        ("train_ablation_head.py", "消融3 - Head ARConv"),
        ("train_ablation_full.py", "完整版 - 全部ARConv"),
    ]
    
    print("\n" + "="*70)
    print("ARConv消融实验批量运行")
    print(f"总共 {len(experiments)} 个实验")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    total_start_time = time.time()
    results = []
    
    for i, (script, name) in enumerate(experiments, 1):
        print(f"\n进度: {i}/{len(experiments)}")
        success = run_experiment(script, name)
        results.append((name, success))
        
        # 如果某个实验失败，询问是否继续
        if not success:
            response = input("\n实验失败，是否继续下一个实验？(y/n): ")
            if response.lower() != 'y':
                print("用户中止实验")
                break
    
    # 打印总结
    total_elapsed = time.time() - total_start_time
    total_hours = int(total_elapsed // 3600)
    total_minutes = int((total_elapsed % 3600) // 60)
    
    print("\n" + "="*70)
    print("所有实验完成！")
    print(f"总耗时: {total_hours}小时 {total_minutes}分钟")
    print("\n实验结果:")
    print("-"*70)
    
    for name, success in results:
        status = "✓ 成功" if success else "✗ 失败"
        print(f"{status} - {name}")
    
    print("="*70)
    print("\n结果保存在: runs/ablation/")
    print("  - baseline/          (基线)")
    print("  - arconv_backbone/   (消融1)")
    print("  - arconv_neck/       (消融2)")
    print("  - arconv_head/       (消融3)")
    print("  - arconv_full/       (完整版)")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
