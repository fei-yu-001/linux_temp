#!/usr/bin/env python3
"""
解析消融实验结果的脚本
用于分析从AutoDL服务器下载的ablation_results.tar.gz中的数据
"""

import pandas as pd
import os

def parse_results_csv(csv_path, exp_name):
    """解析单个实验的results.csv文件"""
    try:
        df = pd.read_csv(csv_path)
        
        # 找到mAP50最高的epoch
        if 'metrics/mAP50(B)' in df.columns:
            best_idx = df['metrics/mAP50(B)'].idxmax()
            best_row = df.loc[best_idx]
            
            print(f"\n{'='*60}")
            print(f"实验名称: {exp_name}")
            print(f"{'='*60}")
            print(f"最佳Epoch: {int(best_row['epoch'])}")
            print(f"训练轮数: {len(df)}")
            print(f"\n性能指标:")
            print(f"  mAP50:     {best_row['metrics/mAP50(B)']:.4f} ({best_row['metrics/mAP50(B)']*100:.2f}%)")
            print(f"  mAP50-95:  {best_row['metrics/mAP50-95(B)']:.4f} ({best_row['metrics/mAP50-95(B)']*100:.2f}%)")
            print(f"  Precision: {best_row['metrics/precision(B)']:.4f} ({best_row['metrics/precision(B)']*100:.2f}%)")
            print(f"  Recall:    {best_row['metrics/recall(B)']:.4f} ({best_row['metrics/recall(B)']*100:.2f}%)")
            
            return {
                'name': exp_name,
                'epoch': int(best_row['epoch']),
                'total_epochs': len(df),
                'mAP50': best_row['metrics/mAP50(B)'],
                'mAP50_95': best_row['metrics/mAP50-95(B)'],
                'precision': best_row['metrics/precision(B)'],
                'recall': best_row['metrics/recall(B)']
            }
        else:
            print(f"\n警告: {exp_name} 的CSV文件格式不正确")
            return None
            
    except Exception as e:
        print(f"\n错误: 无法解析 {exp_name}: {str(e)}")
        return None

def main():
    # 定义实验列表
    experiments = [
        ('arconv_head', 'ARConv Head（检测头）'),
        ('arconv_neck', 'ARConv Neck（颈部网络）'),
        ('arconv_backbone', 'ARConv Backbone（骨干网络）'),
        ('arconv_backbone2', 'ARConv Backbone2（骨干网络-第2次）'),
        ('arconv_full', 'ARConv Full（完全替换）')
    ]
    
    results_dir = 'ablation_results'
    
    # 检查目录是否存在
    if not os.path.exists(results_dir):
        print(f"错误: 找不到目录 {results_dir}")
        print("请先解压 ablation_results.tar.gz 文件")
        return
    
    all_results = []
    
    print("\n" + "="*60)
    print("消融实验结果分析")
    print("="*60)
    
    # 解析每个实验
    for exp_file, exp_name in experiments:
        csv_path = os.path.join(results_dir, f'{exp_file}_results.csv')
        if os.path.exists(csv_path):
            result = parse_results_csv(csv_path, exp_name)
            if result:
                all_results.append(result)
        else:
            print(f"\n警告: 找不到文件 {csv_path}")
    
    # 对比分析
    if len(all_results) >= 2:
        print(f"\n{'='*60}")
        print("性能对比分析")
        print(f"{'='*60}")
        
        # 按mAP50排序
        sorted_results = sorted(all_results, key=lambda x: x['mAP50'], reverse=True)
        
        print("\nmAP50排名:")
        for i, result in enumerate(sorted_results, 1):
            print(f"{i}. {result['name']}: {result['mAP50']*100:.2f}%")
        
        # 找到基线（如果有的话，通常是最低的）
        baseline = min(all_results, key=lambda x: x['mAP50'])
        
        print(f"\n以 {baseline['name']} 为基线的提升:")
        for result in sorted_results:
            if result['name'] != baseline['name']:
                improvement = (result['mAP50'] - baseline['mAP50']) / baseline['mAP50'] * 100
                print(f"  {result['name']}: +{improvement:.2f}%")

if __name__ == '__main__':
    main()
