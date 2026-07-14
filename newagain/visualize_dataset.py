#!/usr/bin/env python3
"""
数据集可视化脚本
用于分析和可视化domestic_dataset数据集
"""

import os
import cv2
import yaml
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict, Counter
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class DatasetVisualizer:
    def __init__(self, data_yaml_path):
        """初始化数据集可视化器"""
        with open(data_yaml_path, 'r', encoding='utf-8') as f:
            self.data_config = yaml.safe_load(f)
        
        self.dataset_root = Path(data_yaml_path).parent
        self.nc = self.data_config['nc']
        self.names = self.data_config['names']
        
        print(f"✅ 加载数据集配置: {self.nc}个类别")
        print(f"📁 数据集路径: {self.dataset_root}")
    
    def load_annotations(self, split='train'):
        """加载标注信息"""
        img_dir = self.dataset_root / 'images' / split
        label_dir = self.dataset_root / 'labels' / split
        
        if not img_dir.exists():
            print(f"❌ 图片目录不存在: {img_dir}")
            return None
        
        annotations = {
            'class_counts': Counter(),
            'bbox_sizes': [],
            'objects_per_image': [],
            'class_cooccurrence': np.zeros((self.nc, self.nc)),
            'images': []
        }
        
        label_files = list(label_dir.glob('*.txt'))
        print(f"📊 正在分析 {len(label_files)} 个标注文件...")
        
        for label_file in label_files:
            img_file = img_dir / (label_file.stem + '.jpg')
            if not img_file.exists():
                img_file = img_dir / (label_file.stem + '.png')
            
            if not img_file.exists():
                continue
            
            # 读取标注
            with open(label_file, 'r') as f:
                lines = f.readlines()
            
            if len(lines) == 0:
                continue
            
            classes_in_image = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                
                cls_id = int(parts[0])
                x_center, y_center, width, height = map(float, parts[1:5])
                
                annotations['class_counts'][cls_id] += 1
                annotations['bbox_sizes'].append((width, height))
                classes_in_image.append(cls_id)
            
            annotations['objects_per_image'].append(len(lines))
            
            # 记录类别共现
            for i, cls1 in enumerate(classes_in_image):
                for cls2 in classes_in_image[i:]:
                    annotations['class_cooccurrence'][cls1][cls2] += 1
                    if cls1 != cls2:
                        annotations['class_cooccurrence'][cls2][cls1] += 1
            
            # 保存图片路径用于后续展示
            annotations['images'].append({
                'path': str(img_file),
                'label_path': str(label_file),
                'classes': classes_in_image
            })
        
        return annotations
    
    def plot_class_distribution(self, train_ann, val_ann=None, test_ann=None, save_path='class_distribution.png'):
        """绘制类别分布图"""
        fig, ax = plt.subplots(figsize=(20, 8))
        
        class_ids = list(range(self.nc))
        train_counts = [train_ann['class_counts'].get(i, 0) for i in class_ids]
        
        if val_ann and test_ann:
            val_counts = [val_ann['class_counts'].get(i, 0) for i in class_ids]
            test_counts = [test_ann['class_counts'].get(i, 0) for i in class_ids]
            x = np.arange(len(class_ids))
            width = 0.25
            
            ax.bar(x - width, train_counts, width, label='训练集', color='skyblue')
            ax.bar(x, val_counts, width, label='验证集', color='lightcoral')
            ax.bar(x + width, test_counts, width, label='测试集', color='lightgreen')
        elif val_ann:
            val_counts = [val_ann['class_counts'].get(i, 0) for i in class_ids]
            x = np.arange(len(class_ids))
            width = 0.35
            
            ax.bar(x - width/2, train_counts, width, label='训练集', color='skyblue')
            ax.bar(x + width/2, val_counts, width, label='验证集', color='lightcoral')
        else:
            ax.bar(class_ids, train_counts, color='skyblue')
        
        ax.set_xlabel('类别', fontsize=12)
        ax.set_ylabel('样本数量', fontsize=12)
        ax.set_title('数据集类别分布', fontsize=14, fontweight='bold')
        ax.set_xticks(class_ids)
        ax.set_xticklabels([self.names[i] for i in class_ids], rotation=90, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        if val_ann or test_ann:
            ax.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 保存类别分布图: {save_path}")
        plt.close()
    
    def plot_bbox_size_distribution(self, annotations, save_path='bbox_size_distribution.png'):
        """绘制标注框尺寸分布"""
        if not annotations['bbox_sizes']:
            print("⚠️ 没有标注框数据")
            return
        
        widths, heights = zip(*annotations['bbox_sizes'])
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # 散点图
        axes[0].scatter(widths, heights, alpha=0.3, s=10)
        axes[0].set_xlabel('宽度 (归一化)', fontsize=12)
        axes[0].set_ylabel('高度 (归一化)', fontsize=12)
        axes[0].set_title('标注框尺寸分布', fontsize=14, fontweight='bold')
        axes[0].grid(alpha=0.3)
        
        # 宽度直方图
        axes[1].hist(widths, bins=50, color='skyblue', edgecolor='black')
        axes[1].set_xlabel('宽度 (归一化)', fontsize=12)
        axes[1].set_ylabel('数量', fontsize=12)
        axes[1].set_title('标注框宽度分布', fontsize=14, fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)
        
        # 高度直方图
        axes[2].hist(heights, bins=50, color='lightcoral', edgecolor='black')
        axes[2].set_xlabel('高度 (归一化)', fontsize=12)
        axes[2].set_ylabel('数量', fontsize=12)
        axes[2].set_title('标注框高度分布', fontsize=14, fontweight='bold')
        axes[2].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 保存标注框尺寸分布图: {save_path}")
        plt.close()
    
    def plot_objects_per_image(self, annotations, save_path='objects_per_image.png'):
        """绘制每张图片的目标数量分布"""
        if not annotations['objects_per_image']:
            print("⚠️ 没有目标数量数据")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        counts = Counter(annotations['objects_per_image'])
        x = sorted(counts.keys())
        y = [counts[i] for i in x]
        
        ax.bar(x, y, color='lightgreen', edgecolor='black')
        ax.set_xlabel('每张图片的目标数量', fontsize=12)
        ax.set_ylabel('图片数量', fontsize=12)
        ax.set_title('每张图片目标数量分布', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # 添加统计信息
        mean_obj = np.mean(annotations['objects_per_image'])
        median_obj = np.median(annotations['objects_per_image'])
        ax.axvline(mean_obj, color='red', linestyle='--', linewidth=2, label=f'平均值: {mean_obj:.1f}')
        ax.axvline(median_obj, color='blue', linestyle='--', linewidth=2, label=f'中位数: {median_obj:.1f}')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 保存目标数量分布图: {save_path}")
        plt.close()
    
    def plot_sample_grid(self, annotations, save_path='sample_grid.png', samples_per_class=2):
        """绘制样本展示网格"""
        # 为每个类别选择样本
        class_samples = defaultdict(list)
        for img_info in annotations['images']:
            for cls_id in set(img_info['classes']):
                if len(class_samples[cls_id]) < samples_per_class:
                    class_samples[cls_id].append(img_info)
        
        # 计算网格大小
        n_classes = min(16, self.nc)  # 最多显示16个类别
        n_cols = 4
        n_rows = (n_classes + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5*n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
        
        for idx in range(n_classes):
            ax = axes[idx]
            
            if idx not in class_samples or not class_samples[idx]:
                ax.axis('off')
                continue
            
            # 读取第一张样本图片
            img_info = class_samples[idx][0]
            img = cv2.imread(img_info['path'])
            if img is None:
                ax.axis('off')
                continue
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w = img.shape[:2]
            
            # 绘制标注框
            with open(img_info['label_path'], 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    
                    cls_id = int(parts[0])
                    if cls_id != idx:
                        continue
                    
                    x_center, y_center, width, height = map(float, parts[1:5])
                    x1 = int((x_center - width/2) * w)
                    y1 = int((y_center - height/2) * h)
                    x2 = int((x_center + width/2) * w)
                    y2 = int((y_center + height/2) * h)
                    
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            
            ax.imshow(img)
            ax.set_title(f'{self.names[idx]}', fontsize=10)
            ax.axis('off')
        
        # 隐藏多余的子图
        for idx in range(n_classes, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 保存样本网格图: {save_path}")
        plt.close()
    
    def print_statistics(self, train_ann, val_ann=None, test_ann=None):
        """打印数据集统计信息"""
        print("\n" + "="*70)
        print("📊 数据集统计信息")
        print("="*70)
        
        print(f"\n类别数量: {self.nc}")
        print(f"训练集图片数: {len(train_ann['images'])}")
        print(f"训练集目标数: {sum(train_ann['class_counts'].values())}")
        
        if val_ann:
            print(f"验证集图片数: {len(val_ann['images'])}")
            print(f"验证集目标数: {sum(val_ann['class_counts'].values())}")
        
        if test_ann:
            print(f"测试集图片数: {len(test_ann['images'])}")
            print(f"测试集目标数: {sum(test_ann['class_counts'].values())}")
        
        total_images = len(train_ann['images'])
        if val_ann:
            total_images += len(val_ann['images'])
        if test_ann:
            total_images += len(test_ann['images'])
        print(f"\n总图片数: {total_images}")
        
        print(f"\n平均每张图片目标数: {np.mean(train_ann['objects_per_image']):.2f}")
        print(f"最多目标数: {max(train_ann['objects_per_image'])}")
        print(f"最少目标数: {min(train_ann['objects_per_image'])}")
        
        # 类别统计
        print(f"\n样本最多的类别:")
        for cls_id, count in train_ann['class_counts'].most_common(5):
            print(f"  {self.names[cls_id]}: {count}")
        
        print(f"\n样本最少的类别:")
        for cls_id, count in train_ann['class_counts'].most_common()[-5:]:
            print(f"  {self.names[cls_id]}: {count}")
        
        print("\n" + "="*70)

def main():
    """主函数"""
    # 数据集配置文件路径
    data_yaml = 'ultralytics-main/domestic_dataset/data.yaml'
    
    if not os.path.exists(data_yaml):
        print(f"❌ 找不到数据集配置文件: {data_yaml}")
        print("请确保数据集路径正确")
        return
    
    # 创建可视化器
    visualizer = DatasetVisualizer(data_yaml)
    
    # 加载训练集标注
    print("\n📊 加载训练集标注...")
    train_ann = visualizer.load_annotations('train')
    
    if train_ann is None:
        print("❌ 无法加载训练集标注")
        return
    
    # 加载验证集标注
    print("\n📊 加载验证集标注...")
    val_ann = visualizer.load_annotations('val')
    
    # 加载测试集标注
    print("\n📊 加载测试集标注...")
    test_ann = visualizer.load_annotations('test')
    
    # 打印统计信息
    visualizer.print_statistics(train_ann, val_ann, test_ann)
    
    # 创建输出目录
    output_dir = Path('dataset_visualization')
    output_dir.mkdir(exist_ok=True)
    
    # 生成可视化图表
    print("\n📊 生成可视化图表...")
    
    visualizer.plot_class_distribution(
        train_ann, val_ann, test_ann,
        save_path=output_dir / 'class_distribution.png'
    )
    
    visualizer.plot_bbox_size_distribution(
        train_ann,
        save_path=output_dir / 'bbox_size_distribution.png'
    )
    
    visualizer.plot_objects_per_image(
        train_ann,
        save_path=output_dir / 'objects_per_image.png'
    )
    
    visualizer.plot_sample_grid(
        train_ann,
        save_path=output_dir / 'sample_grid.png',
        samples_per_class=1
    )
    
    print(f"\n✅ 所有可视化图表已保存到: {output_dir}")
    print("\n" + "="*70)
    print("完成！")
    print("="*70)

if __name__ == '__main__':
    main()
