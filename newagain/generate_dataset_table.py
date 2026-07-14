#!/usr/bin/env python3
"""
生成数据集统计表格
用于论文中的表2：典型害虫类别样本分布
"""

import yaml
from pathlib import Path
from collections import Counter

def load_annotations(dataset_root, split='train'):
    """加载标注信息"""
    label_dir = dataset_root / 'labels' / split
    
    class_counts = Counter()
    label_files = list(label_dir.glob('*.txt'))
    
    for label_file in label_files:
        with open(label_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    cls_id = int(parts[0])
                    class_counts[cls_id] += 1
    
    return class_counts

def main():
    # 数据集路径
    data_yaml = Path('ultralytics-main/domestic_dataset/data.yaml')
    dataset_root = data_yaml.parent
    
    # 加载配置
    with open(data_yaml, 'r', encoding='utf-8') as f:
        data_config = yaml.safe_load(f)
    
    names = data_config['names']
    nc = data_config['nc']
    
    print("📊 正在统计数据集...")
    
    # 加载各个数据集的统计
    train_counts = load_annotations(dataset_root, 'train')
    val_counts = load_annotations(dataset_root, 'val')
    test_counts = load_annotations(dataset_root, 'test')
    
    # 计算总数
    total_train = sum(train_counts.values())
    total_val = sum(val_counts.values())
    total_test = sum(test_counts.values())
    total_all = total_train + total_val + total_test
    
    # 找出Cicadellidae和aphids的索引
    cicadellidae_idx = None
    aphids_idx = None
    
    for i, name in enumerate(names):
        if name == 'Cicadellidae':
            cicadellidae_idx = i
        elif name == 'aphids':
            aphids_idx = i
    
    print("\n" + "="*80)
    print("表2 典型害虫类别样本分布")
    print("="*80)
    print(f"{'类别名称':<20} {'训练集':>10} {'验证集':>10} {'测试集':>10} {'总计':>10} {'占比':>10}")
    print("-"*80)
    
    # 打印Cicadellidae
    if cicadellidae_idx is not None:
        train = train_counts.get(cicadellidae_idx, 0)
        val = val_counts.get(cicadellidae_idx, 0)
        test = test_counts.get(cicadellidae_idx, 0)
        total = train + val + test
        ratio = (total / total_all) * 100
        print(f"{'Cicadellidae':<20} {train:>10,} {val:>10,} {test:>10,} {total:>10,} {ratio:>9.1f}%")
    
    # 打印aphids
    if aphids_idx is not None:
        train = train_counts.get(aphids_idx, 0)
        val = val_counts.get(aphids_idx, 0)
        test = test_counts.get(aphids_idx, 0)
        total = train + val + test
        ratio = (total / total_all) * 100
        print(f"{'aphids':<20} {train:>10,} {val:>10,} {test:>10,} {total:>10,} {ratio:>9.1f}%")
    
    print("-"*80)
    
    # 打印总计行
    print(f"{'全部类别':<20} {total_train:>10,} {total_val:>10,} {total_test:>10,} {total_all:>10,} {'100.0%':>10}")
    
    print("="*80)
    
    # 生成Markdown格式
    print("\n\n📝 Markdown格式（可直接复制到论文）：")
    print("\n```markdown")
    print("表2 典型害虫类别样本分布\n")
    print("| 类别名称      | 训练集  | 验证集 | 测试集 | 总计   | 占比   |")
    print("|--------------|--------|--------|--------|--------|--------|")
    
    # Cicadellidae
    if cicadellidae_idx is not None:
        train = train_counts.get(cicadellidae_idx, 0)
        val = val_counts.get(cicadellidae_idx, 0)
        test = test_counts.get(cicadellidae_idx, 0)
        total = train + val + test
        ratio = (total / total_all) * 100
        print(f"| Cicadellidae | {train:,}  | {val:>3,}    | {test:>3,}    | {total:,}  | {ratio:.1f}%  |")
    
    # aphids
    if aphids_idx is not None:
        train = train_counts.get(aphids_idx, 0)
        val = val_counts.get(aphids_idx, 0)
        test = test_counts.get(aphids_idx, 0)
        total = train + val + test
        ratio = (total / total_all) * 100
        print(f"| aphids       | {train:>3,}    | {val:>3,}    | {test:>3,}    | {total:,}  | {ratio:.1f}%   |")
    
    # 总计
    print(f"| **全部类别** | **{total_train:,}** | **{total_val:,}** | **{total_test:,}** | **{total_all:,}** | **100.0%** |")
    print("```")
    
    # 生成LaTeX格式
    print("\n\n📝 LaTeX格式（可直接复制到论文）：")
    print("\n```latex")
    print("\\begin{table}[htbp]")
    print("\\centering")
    print("\\caption{典型害虫类别样本分布}")
    print("\\label{tab:dataset_distribution}")
    print("\\begin{tabular}{lccccc}")
    print("\\hline")
    print("类别名称 & 训练集 & 验证集 & 测试集 & 总计 & 占比 \\\\")
    print("\\hline")
    
    # Cicadellidae
    if cicadellidae_idx is not None:
        train = train_counts.get(cicadellidae_idx, 0)
        val = val_counts.get(cicadellidae_idx, 0)
        test = test_counts.get(cicadellidae_idx, 0)
        total = train + val + test
        ratio = (total / total_all) * 100
        print(f"Cicadellidae & {train:,} & {val:,} & {test:,} & {total:,} & {ratio:.1f}\\% \\\\")
    
    # aphids
    if aphids_idx is not None:
        train = train_counts.get(aphids_idx, 0)
        val = val_counts.get(aphids_idx, 0)
        test = test_counts.get(aphids_idx, 0)
        total = train + val + test
        ratio = (total / total_all) * 100
        print(f"aphids & {train:,} & {val:,} & {test:,} & {total:,} & {ratio:.1f}\\% \\\\")
    
    print("\\hline")
    print(f"\\textbf{{全部类别}} & \\textbf{{{total_train:,}}} & \\textbf{{{total_val:,}}} & \\textbf{{{total_test:,}}} & \\textbf{{{total_all:,}}} & \\textbf{{100.0\\%}} \\\\")
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}")
    print("```")
    
    print("\n✅ 完成！")

if __name__ == '__main__':
    main()
