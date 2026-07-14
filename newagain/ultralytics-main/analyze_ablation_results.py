#!/usr/bin/env python3
"""
ARConv消融实验结果分析脚本
分析和比较所有消融实验的结果
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

def load_results(experiment_name):
    """加载单个实验的结果"""
    results_path = f'runs/ablation/{experiment_name}/results.csv'
    
    if not os.path.exists(results_path):
        print(f"警告: 找不到 {results_path}")
        return None
    
    df = pd.read_csv(results_path)
    df = df.apply(pd.to_numeric, errors='ignore')
    
    # 获取最后一个epoch的结果
    last_row = df.iloc[-1]
    
    return {
        'name': experiment_name,
        'mAP50': last_row.get('metrics/mAP50(B)', 0),
        'mAP50-95': last_row.get('metrics/mAP50-95(B)', 0),
        'precision': last_row.get('metrics/precision(B)', 0),
        'recall': last_row.get('metrics/recall(B)', 0),
        'box_loss': last_row.get('train/box_loss', 0),
        'cls_loss': last_row.get('train/cls_loss', 0),
        'dfl_loss': last_row.get('train/dfl_loss', 0),
    }

def main():
    """主函数"""
    
    experiments = [
        ('baseline', '基线'),
        ('arconv_backbone', 'Backbone ARConv'),
        ('arconv_neck', 'Neck ARConv'),
        ('arconv_head', 'Head ARConv'),
        ('arconv_full', '完整ARConv'),
    ]
    
    print("\n" + "="*70)
    print("ARConv消融实验结果分析")
    print("="*70 + "\n")
    
    # 加载所有结果
    results = []
    for exp_name, display_name in experiments:
        result = load_results(exp_name)
        if result:
            result['display_name'] = display_name
            results.append(result)
    
    if not results:
        print("错误: 没有找到任何实验结果")
        return
    
    # 创建DataFrame
    df = pd.DataFrame(results)
    
    # 打印结果表格
    print("实验结果对比:")
    print("-"*70)
    print(f"{'实验名称':<20} {'mAP50':<10} {'mAP50-95':<10} {'Precision':<10} {'Recall':<10}")
    print("-"*70)
    
    for _, row in df.iterrows():
        print(f"{row['display_name']:<20} "
              f"{row['mAP50']:<10.4f} "
              f"{row['mAP50-95']:<10.4f} "
              f"{row['precision']:<10.4f} "
              f"{row['recall']:<10.4f}")
    
    print("-"*70)
    
    # 找出最佳模型
    best_map50 = df.loc[df['mAP50'].idxmax()]
    best_map50_95 = df.loc[df['mAP50-95'].idxmax()]
    
    print(f"\n最佳 mAP50: {best_map50['display_name']} ({best_map50['mAP50']:.4f})")
    print(f"最佳 mAP50-95: {best_map50_95['display_name']} ({best_map50_95['mAP50-95']:.4f})")
    
    # 绘制对比图
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # mAP50对比
    axes[0, 0].bar(df['display_name'], df['mAP50'], color='skyblue')
    axes[0, 0].set_title('mAP50 对比', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('mAP50')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # mAP50-95对比
    axes[0, 1].bar(df['display_name'], df['mAP50-95'], color='lightcoral')
    axes[0, 1].set_title('mAP50-95 对比', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('mAP50-95')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Precision对比
    axes[1, 0].bar(df['display_name'], df['precision'], color='lightgreen')
    axes[1, 0].set_title('Precision 对比', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Precision')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Recall对比
    axes[1, 1].bar(df['display_name'], df['recall'], color='plum')
    axes[1, 1].set_title('Recall 对比', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Recall')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ablation_comparison.png', dpi=300, bbox_inches='tight')
    print(f"\n对比图已保存: ablation_comparison.png")
    
    # 绘制Loss对比
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    axes[0].bar(df['display_name'], df['box_loss'], color='orange')
    axes[0].set_title('Box Loss 对比', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Box Loss')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', alpha=0.3)
    
    axes[1].bar(df['display_name'], df['cls_loss'], color='cyan')
    axes[1].set_title('Classification Loss 对比', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Cls Loss')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y', alpha=0.3)
    
    axes[2].bar(df['display_name'], df['dfl_loss'], color='pink')
    axes[2].set_title('DFL Loss 对比', fontsize=14, fontweight='bold')
    axes[2].set_ylabel('DFL Loss')
    axes[2].tick_params(axis='x', rotation=45)
    axes[2].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ablation_loss_comparison.png', dpi=300, bbox_inches='tight')
    print(f"Loss对比图已保存: ablation_loss_comparison.png")
    
    print("\n" + "="*70)
    print("分析完成！")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
