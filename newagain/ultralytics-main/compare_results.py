"""
对比所有模型的训练结果
使用方法：python compare_results.py
"""
import os
import pandas as pd
from pathlib import Path

def read_results(exp_name):
    """读取单个实验的结果"""
    results_file = Path(f'runs/train/{exp_name}/results.csv')
    
    if not results_file.exists():
        print(f"警告: {exp_name} 的结果文件不存在")
        return None
    
    try:
        df = pd.read_csv(results_file)
        # 获取最后一个epoch的结果
        last_row = df.iloc[-1]
        
        return {
            'Model': exp_name,
            'mAP50': f"{last_row.get('metrics/mAP50(B)', 0):.4f}",
            'mAP50-95': f"{last_row.get('metrics/mAP50-95(B)', 0):.4f}",
            'Precision': f"{last_row.get('metrics/precision(B)', 0):.4f}",
            'Recall': f"{last_row.get('metrics/recall(B)', 0):.4f}",
            'Train Loss': f"{last_row.get('train/box_loss', 0):.4f}",
            'Val Loss': f"{last_row.get('val/box_loss', 0):.4f}",
        }
    except Exception as e:
        print(f"读取 {exp_name} 结果时出错: {e}")
        return None

def main():
    # 定义所有实验名称
    experiments = [
        'yolov8n_domestic',
        'yolo11n_domestic',
        'yolo12n_domestic',
        'yolov9c_domestic',
        'yolov10n_domestic',
    ]
    
    print("="*80)
    print("YOLO模型对比实验 - 结果汇总")
    print("="*80)
    
    results = []
    for exp_name in experiments:
        result = read_results(exp_name)
        if result:
            results.append(result)
    
    if not results:
        print("没有找到任何结果文件！")
        print("请确保已经运行了训练脚本，并且结果保存在 runs/train/ 目录下")
        return
    
    # 创建DataFrame并显示
    df = pd.DataFrame(results)
    
    print("\n训练结果对比:")
    print("-"*80)
    print(df.to_string(index=False))
    print("-"*80)
    
    # 找出最佳模型
    print("\n最佳模型:")
    
    # 转换为数值类型进行比较
    df_numeric = df.copy()
    for col in ['mAP50', 'mAP50-95', 'Precision', 'Recall']:
        df_numeric[col] = df_numeric[col].astype(float)
    
    best_map50 = df_numeric.loc[df_numeric['mAP50'].idxmax(), 'Model']
    best_map50_95 = df_numeric.loc[df_numeric['mAP50-95'].idxmax(), 'Model']
    best_precision = df_numeric.loc[df_numeric['Precision'].idxmax(), 'Model']
    best_recall = df_numeric.loc[df_numeric['Recall'].idxmax(), 'Model']
    
    print(f"  • 最高 mAP50: {best_map50}")
    print(f"  • 最高 mAP50-95: {best_map50_95}")
    print(f"  • 最高 Precision: {best_precision}")
    print(f"  • 最高 Recall: {best_recall}")
    
    # 保存对比结果
    output_file = 'runs/train/comparison_results.csv'
    df.to_csv(output_file, index=False)
    print(f"\n对比结果已保存到: {output_file}")
    print("="*80)

if __name__ == '__main__':
    main()
