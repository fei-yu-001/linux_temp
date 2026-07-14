#!/usr/bin/env python3
"""
ARConv消融实验结果分析脚本
分析和可视化消融实验结果
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_latest_results():
    """加载最新的实验结果"""
    results_dir = Path('runs/ablation/summary')
    
    if not results_dir.exists():
        print("❌ 未找到实验结果目录")
        return None
    
    # 查找最新的JSON文件
    json_files = list(results_dir.glob('ablation_results_*.json'))
    
    if not json_files:
        print("❌ 未找到实验结果文件")
        return None
    
    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    print(f"📂 加载结果文件: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_comparison_dataframe(results):
    """创建对比数据框"""
    experiments = results['experiments']
    
    data = []
    for exp_name, exp_result in experiments.items():
        if exp_result['success'] and exp_result['metrics']:
            # 确定替换位置
            if 'backbone' in exp_name:
                location = 'Backbone'
            elif 'neck' in exp_name:
                location = 'Neck'
            elif 'head' in exp_name:
                location = 'Head'
            elif 'full' in exp_name:
                location = 'All'
            else:
                location = 'Unknown'
            
            data.append({
                '实验名称': exp_name,
                '替换位置': location,
                'mAP50': exp_result['metrics']['mAP50'],
                'mAP50-95': exp_result['metrics']['mAP50-95'],
                'Precision': exp_result['metrics']['precision'],
                'Recall': exp_result['metrics']['recall'],
                '最佳Epoch': exp_result['metrics']['best_epoch'],
                '训练时间(h)': exp_result['duration_hours'],
            })
    
    df = pd.DataFrame(data)
    
    # 按位置排序：Backbone -> Neck -> Head -> All
    location_order = {'Backbone': 1, 'Neck': 2, 'Head': 3, 'All': 4}
    df['sort_key'] = df['替换位置'].map(location_order)
    df = df.sort_values('sort_key').drop('sort_key', axis=1)
    
    return df


def plot_metrics_comparison(df, save_dir):
    """绘制指标对比图"""
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. mAP50对比柱状图
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['实验名称'], df['mAP50'], color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'])
    ax.set_xlabel('实验', fontsize=12)
    ax.set_ylabel('mAP50', fontsize=12)
    ax.set_title('ARConv消融实验 - mAP50对比', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # 在柱子上显示数值
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(save_dir / 'map50_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✅ 保存图表: {save_dir / 'map50_comparison.png'}")
    plt.close()
    
    # 2. 多指标对比雷达图
    if len(df) >= 2:
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        metrics = ['mAP50', 'mAP50-95', 'Precision', 'Recall']
        angles = [n / len(metrics) * 2 * 3.14159 for n in range(len(metrics))]
        angles += angles[:1]
        
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
        
        for idx, row in df.iterrows():
            values = [row[m] for m in metrics]
            values += values[:1]
            ax.plot(angles, values, 'o-', linewidth=2, label=row['实验名称'], color=colors[idx % len(colors)])
            ax.fill(angles, values, alpha=0.15, color=colors[idx % len(colors)])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=11)
        ax.set_ylim(0, 1)
        ax.set_title('ARConv消融实验 - 多指标对比', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_dir / 'metrics_radar.png', dpi=300, bbox_inches='tight')
        print(f"✅ 保存图表: {save_dir / 'metrics_radar.png'}")
        plt.close()
    
    # 3. 不同部位性能对比图
    if len(df) >= 2:
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # 为每个位置设置颜色
        colors = {'Backbone': '#3498db', 'Neck': '#2ecc71', 'Head': '#f39c12', 'All': '#e74c3c'}
        
        x_pos = range(len(df))
        bars = ax.bar(x_pos, df['mAP50'], color=[colors.get(loc, '#95a5a6') for loc in df['替换位置']])
        
        ax.set_xlabel('实验', fontsize=12)
        ax.set_ylabel('mAP50', fontsize=12)
        ax.set_title('ARConv消融实验 - 不同部位性能对比', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(df['替换位置'], fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        
        # 在柱子上显示数值
        for i, (bar, val) in enumerate(zip(bars, df['mAP50'])):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.4f}',
                   ha='center', va='bottom', fontsize=10)
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=colors[loc], label=loc) 
                          for loc in ['Backbone', 'Neck', 'Head', 'All'] if loc in df['替换位置'].values]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(save_dir / 'location_comparison.png', dpi=300, bbox_inches='tight')
        print(f"✅ 保存图表: {save_dir / 'location_comparison.png'}")
        plt.close()
    
    # 4. 训练时间对比
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['实验名称'], df['训练时间(h)'], color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'])
    ax.set_xlabel('实验', fontsize=12)
    ax.set_ylabel('训练时间 (小时)', fontsize=12)
    ax.set_title('ARConv消融实验 - 训练时间对比', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    # 在柱子上显示数值
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}h',
                ha='center', va='bottom', fontsize=10)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(save_dir / 'training_time.png', dpi=300, bbox_inches='tight')
    print(f"✅ 保存图表: {save_dir / 'training_time.png'}")
    plt.close()


def print_summary(results, df):
    """打印实验总结"""
    print("\n" + "="*80)
    print("📊 ARConv消融实验总结")
    print("="*80)
    
    print(f"\n⏱️  总耗时: {results['total_duration_hours']:.2f} 小时")
    print(f"💰 预计成本: ¥{results['total_cost_estimate']:.2f}")
    print(f"📅 开始时间: {results['total_start_time']}")
    print(f"📅 结束时间: {results['total_end_time']}")
    
    print("\n" + "="*80)
    print("📈 性能对比")
    print("="*80)
    print(df.to_string(index=False))
    
    # 找出最佳模型
    if not df.empty:
        best_idx = df['mAP50'].idxmax()
        best_model = df.loc[best_idx]
        
        print("\n" + "="*80)
        print("🏆 最佳模型")
        print("="*80)
        print(f"实验名称: {best_model['实验名称']}")
        print(f"ARConv层数: {best_model['ARConv层数']}")
        print(f"mAP50: {best_model['mAP50']:.4f}")
        print(f"mAP50-95: {best_model['mAP50-95']:.4f}")
        if 'mAP50提升%' in best_model:
            print(f"相对基线提升: {best_model['mAP50提升%']:+.2f}%")
        print(f"训练时间: {best_model['训练时间(h)']:.2f} 小时")
    
    print("\n" + "="*80)


def main():
    """主函数"""
    print("="*80)
    print("📊 ARConv消融实验结果分析")
    print("="*80)
    
    # 加载结果
    results = load_latest_results()
    if results is None:
        sys.exit(1)
    
    # 创建对比数据框
    df = create_comparison_dataframe(results)
    
    if df.empty:
        print("❌ 没有成功的实验结果")
        sys.exit(1)
    
    # 打印总结
    print_summary(results, df)
    
    # 绘制图表
    print("\n" + "="*80)
    print("📊 生成可视化图表")
    print("="*80)
    save_dir = Path('runs/ablation/summary/plots')
    plot_metrics_comparison(df, save_dir)
    
    print("\n" + "="*80)
    print("✅ 分析完成！")
    print("="*80)
    print(f"\n图表保存在: {save_dir}")
    print("可以查看以下文件:")
    print("  - map50_comparison.png    (mAP50对比)")
    print("  - metrics_radar.png       (多指标雷达图)")
    print("  - improvement_trend.png   (性能提升趋势)")
    print("  - training_time.png       (训练时间对比)")
    print()


if __name__ == '__main__':
    main()
