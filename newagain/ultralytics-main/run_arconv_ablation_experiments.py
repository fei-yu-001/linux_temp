#!/usr/bin/env python3
"""
ARConv消融实验自动运行脚本 - RTX 4090极致优化版本
自动运行4个实验：Backbone + Neck + Head + Full

预计总时间：约4.8小时
预计总成本：约¥10
"""

import os
import time
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from ultralytics import YOLO
from arconv_callback import arconv_callbacks

# 解决OpenMP库冲突问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 极致优化PyTorch性能（25核CPU优化）
os.environ['CUDA_LAUNCH_BLOCKING'] = '0'
os.environ['TORCH_CUDNN_V8_API_ENABLED'] = '1'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
os.environ['OMP_NUM_THREADS'] = '12'  # 25核用12线程
os.environ['MKL_NUM_THREADS'] = '12'


# 实验配置
EXPERIMENTS = [
    {
        'name': 'arconv_backbone',
        'description': 'ARConv Backbone替换（5层Backbone Conv）',
        'model': 'ultralytics/cfg/models/11/yolo11n_arconv_backbone.yaml',
        'use_arconv': True,
        'location': 'backbone',
        'arconv_layers': 5,
    },
    {
        'name': 'arconv_neck',
        'description': 'ARConv Neck替换（2层Neck Conv）',
        'model': 'ultralytics/cfg/models/11/yolo11n_arconv_neck.yaml',
        'use_arconv': True,
        'location': 'neck',
        'arconv_layers': 2,
    },
    {
        'name': 'arconv_head',
        'description': 'ARConv Head替换（2层Head Conv）',
        'model': 'ultralytics/cfg/models/11/yolo11n_arconv_head.yaml',
        'use_arconv': True,
        'location': 'head',
        'arconv_layers': 2,
    },
    {
        'name': 'arconv_full',
        'description': 'ARConv 全部替换（Backbone + Neck + Head）',
        'model': 'ultralytics/cfg/models/11/yolo11n_arconv_full.yaml',
        'use_arconv': True,
        'location': 'all',
        'arconv_layers': 9,
    },
]

# 训练参数（RTX 4090 25核CPU 90GB内存极致优化）
TRAIN_PARAMS = {
    'data': 'domestic_dataset/data.yaml',
    'epochs': 150,
    'batch': 48,  # 提升到48（90GB内存+RTX 4090）
    'imgsz': 640,
    'device': '0',
    'workers': 12,  # 25核CPU用12个workers
    'cache': True,  # 90GB内存完全够用
    'amp': True,
    'half': False,
    'mosaic': False,
    'close_mosaic': 0,
    'project': 'runs/ablation',
    'patience': 50,
    'save': True,
    'save_period': 15,
    'val': True,
    'plots': True,
    'verbose': True,
    'deterministic': False,
    'rect': False,
}


def print_header(text):
    """打印格式化的标题"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def print_experiment_info(exp_num, total, exp_config):
    """打印实验信息"""
    print_header(f"实验 {exp_num}/{total}: {exp_config['description']}")
    print(f"实验名称: {exp_config['name']}")
    print(f"模型配置: {exp_config['model']}")
    print(f"ARConv层数: {exp_config['arconv_layers']}")
    print(f"使用ARConv: {'是' if exp_config['use_arconv'] else '否'}")
    print()


def train_experiment(exp_config, exp_num, total):
    """训练单个实验"""
    print_experiment_info(exp_num, total, exp_config)
    
    # 记录开始时间
    start_time = time.time()
    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # 加载模型
        print(f"📦 加载模型: {exp_config['model']}")
        model = YOLO(model=exp_config['model'])
        
        # 准备训练参数
        train_params = TRAIN_PARAMS.copy()
        train_params['name'] = exp_config['name']
        
        # 如果使用ARConv，需要在训练前添加回调
        if exp_config['use_arconv']:
            # 不能直接传callbacks参数，需要通过model.add_callback添加
            for event, callback in arconv_callbacks.items():
                model.add_callback(event, callback)
            print("✅ 已添加ARConv回调")
        
        # 开始训练
        print(f"\n🚀 开始训练...")
        print(f"配置: batch={train_params['batch']}, workers={train_params['workers']}, cache={train_params['cache']}")
        print()
        
        results = model.train(**train_params)
        
        # 记录结束时间
        end_time = time.time()
        end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = end_time - start_time
        
        # 获取最佳结果
        results_csv = Path(f"runs/ablation/{exp_config['name']}/results.csv")
        if results_csv.exists():
            df = pd.read_csv(results_csv)
            best_epoch = df['metrics/mAP50(B)'].idxmax()
            best_results = df.iloc[best_epoch]
            
            metrics = {
                'mAP50': float(best_results['metrics/mAP50(B)']),
                'mAP50-95': float(best_results['metrics/mAP50-95(B)']),
                'precision': float(best_results['metrics/precision(B)']),
                'recall': float(best_results['metrics/recall(B)']),
                'best_epoch': int(best_epoch),
            }
        else:
            metrics = None
        
        print(f"\n✅ 实验 {exp_num}/{total} 完成！")
        print(f"训练时间: {duration/3600:.2f} 小时")
        
        if metrics:
            print(f"\n📊 最佳结果 (Epoch {metrics['best_epoch']}):")
            print(f"  mAP50:    {metrics['mAP50']:.4f}")
            print(f"  mAP50-95: {metrics['mAP50-95']:.4f}")
            print(f"  Precision: {metrics['precision']:.4f}")
            print(f"  Recall:    {metrics['recall']:.4f}")
        
        return {
            'success': True,
            'start_time': start_datetime,
            'end_time': end_datetime,
            'duration_hours': duration / 3600,
            'metrics': metrics,
            'error': None,
        }
        
    except KeyboardInterrupt:
        print(f"\n⚠️  实验 {exp_num}/{total} 被用户中断")
        raise
    except Exception as e:
        # 只有真正的错误才标记为失败（不包括训练正常完成）
        if "does not exist" in str(e) or "No such file" in str(e):
            end_time = time.time()
            end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            duration = end_time - start_time
            
            print(f"\n❌ 实验 {exp_num}/{total} 失败！")
            print(f"错误: {str(e)}")
        else:
            # 其他情况可能是训练正常完成，重新抛出以便调试
            print(f"\n⚠️  实验 {exp_num}/{total} 遇到异常: {str(e)}")
            raise
        
        return {
            'success': False,
            'start_time': start_datetime,
            'end_time': end_datetime,
            'duration_hours': duration / 3600,
            'metrics': None,
            'error': str(e),
        }


def save_results(all_results):
    """保存所有实验结果"""
    # 创建结果目录
    results_dir = Path('runs/ablation/summary')
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存JSON格式
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = results_dir / f'ablation_results_{timestamp}.json'
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 结果已保存到: {json_file}")
    
    # 创建对比表格
    comparison_data = []
    for exp_name, result in all_results.items():
        if result['success'] and result['metrics']:
            comparison_data.append({
                '实验名称': exp_name,
                'ARConv层数': next(e['arconv_layers'] for e in EXPERIMENTS if e['name'] == exp_name),
                'mAP50': result['metrics']['mAP50'],
                'mAP50-95': result['metrics']['mAP50-95'],
                'Precision': result['metrics']['precision'],
                'Recall': result['metrics']['recall'],
                '最佳Epoch': result['metrics']['best_epoch'],
                '训练时间(h)': result['duration_hours'],
            })
    
    if comparison_data:
        df = pd.DataFrame(comparison_data)
        
        # 计算相对于基线的提升
        if 'baseline' in all_results and all_results['baseline']['success']:
            baseline_map50 = all_results['baseline']['metrics']['mAP50']
            df['mAP50提升'] = df['mAP50'] - baseline_map50
            df['mAP50提升%'] = (df['mAP50提升'] / baseline_map50 * 100).round(2)
        
        # 保存CSV
        csv_file = results_dir / f'ablation_comparison_{timestamp}.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"📊 对比表格已保存到: {csv_file}")
        
        # 打印对比表格
        print("\n" + "="*80)
        print("📊 消融实验结果对比")
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)
    
    return json_file, csv_file if comparison_data else None


def main():
    """主函数"""
    print_header("🚀 ARConv消融实验自动运行 - RTX 4090极致优化版")
    
    print("实验配置:")
    print(f"  总实验数: {len(EXPERIMENTS)}")
    print(f"  训练轮数: {TRAIN_PARAMS['epochs']}")
    print(f"  Batch Size: {TRAIN_PARAMS['batch']}")
    print(f"  Workers: {TRAIN_PARAMS['workers']}")
    print(f"  Cache: {TRAIN_PARAMS['cache']}")
    print(f"  预计总时间: 约4.0小时")
    print(f"  预计总成本: 约¥8.5")
    print()
    
    print("实验列表:")
    for i, exp in enumerate(EXPERIMENTS, 1):
        print(f"  {i}. {exp['description']}")
    print()
    
    input("按Enter键开始实验...")
    
    # 记录总开始时间
    total_start_time = time.time()
    total_start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 运行所有实验
    all_results = {}
    
    for i, exp_config in enumerate(EXPERIMENTS, 1):
        result = train_experiment(exp_config, i, len(EXPERIMENTS))
        all_results[exp_config['name']] = result
        
        # 如果不是最后一个实验，等待一下
        if i < len(EXPERIMENTS):
            print(f"\n⏳ 等待5秒后开始下一个实验...")
            time.sleep(5)
    
    # 记录总结束时间
    total_end_time = time.time()
    total_end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_duration = total_end_time - total_start_time
    
    # 保存结果
    print_header("💾 保存实验结果")
    
    # 添加总体信息
    summary = {
        'total_start_time': total_start_datetime,
        'total_end_time': total_end_datetime,
        'total_duration_hours': total_duration / 3600,
        'total_cost_estimate': total_duration / 3600 * 2.08,
        'experiments': all_results,
    }
    
    json_file, csv_file = save_results(summary)
    
    # 打印总结
    print_header("🎉 所有实验完成！")
    
    print(f"开始时间: {total_start_datetime}")
    print(f"结束时间: {total_end_datetime}")
    print(f"总耗时: {total_duration/3600:.2f} 小时")
    print(f"预计成本: ¥{total_duration/3600*2.08:.2f}")
    print()
    
    # 统计成功/失败
    success_count = sum(1 for r in all_results.values() if r['success'])
    fail_count = len(all_results) - success_count
    
    print(f"成功: {success_count}/{len(EXPERIMENTS)}")
    print(f"失败: {fail_count}/{len(EXPERIMENTS)}")
    print()
    
    if fail_count > 0:
        print("失败的实验:")
        for exp_name, result in all_results.items():
            if not result['success']:
                print(f"  - {exp_name}: {result['error']}")
        print()
    
    print("结果文件:")
    print(f"  JSON: {json_file}")
    if csv_file:
        print(f"  CSV:  {csv_file}")
    print()
    
    print("="*80)
    print("✅ 实验完成！可以查看 runs/ablation/ 目录下的详细结果")
    print("="*80)


if __name__ == '__main__':
    main()
