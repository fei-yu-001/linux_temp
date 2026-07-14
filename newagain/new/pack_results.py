#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立打包脚本
功能：手动打包已有的训练结果（无需重新训练）

使用方法：
    python pack_results.py              # 打包所有结果
    python pack_results.py --model v5   # 只打包YOLOv5n结果
    python pack_results.py --model v12  # 只打包YOLO12n结果
    python pack_results.py --model v26  # 只打包YOLO26n结果
    python pack_results.py --model v13  # 只打包YOLOv13n结果
"""
import os
import shutil
import argparse
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 各模型结果目录映射
MODEL_MAP = {
    'v5':  {'name': 'YOLOv5n',  'dir': 'ultralytics-latest/runs/train/yolov5n_domestic'},
    'v12': {'name': 'YOLO12n',  'dir': 'ultralytics-latest/runs/train/yolo12n_domestic'},
    'v26': {'name': 'YOLO26n',  'dir': 'ultralytics-latest/runs/train/yolo26n_domestic'},
    'v13': {'name': 'YOLOv13n', 'dir': 'yolov13/runs/train/yolov13n_domestic'},
}

# 需要收集的关键文件
KEY_FILES = [
    'weights/best.pt',
    'weights/last.pt',
    'results.csv',
    'results.png',
    'confusion_matrix.png',
    'labels.jpg',
    'PR_curve.png',
    'F1_curve.png',
    'args.yaml',
]


def pack_model(model_key):
    """打包单个模型结果"""
    info = MODEL_MAP[model_key]
    result_dir = os.path.join(PROJECT_ROOT, info['dir'])
    model_name = info['name']

    if not os.path.isdir(result_dir):
        print(f"  ✗ {model_name}: 结果目录不存在 ({info['dir']})")
        return False

    pack_dir = os.path.join(PROJECT_ROOT, 'packed_results', model_name)
    os.makedirs(pack_dir, exist_ok=True)

    copied = 0
    for f in KEY_FILES:
        src = os.path.join(result_dir, f)
        if os.path.isfile(src):
            dst = os.path.join(pack_dir, os.path.basename(f))
            shutil.copy2(src, dst)
            copied += 1
            print(f"  复制: {model_name}/{os.path.basename(f)} ({os.path.getsize(src)/1024/1024:.1f}MB)")

    # 额外复制整个weights目录（如果存在）
    weights_src = os.path.join(result_dir, 'weights')
    if os.path.isdir(weights_src):
        weights_dst = os.path.join(pack_dir, 'weights')
        if os.path.exists(weights_dst):
            shutil.rmtree(weights_dst)
        shutil.copytree(weights_src, weights_dst)
        print(f"  复制: {model_name}/weights/ (完整目录)")

    print(f"  ✓ {model_name}: 复制了 {copied} 个关键文件")
    return True


def create_tar(pack_dir):
    """创建tar.gz压缩包"""
    tar_name = f"comparison_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    tar_path = os.path.join(PROJECT_ROOT, tar_name)

    print(f"\n  正在打包: {tar_name} ...")

    import subprocess
    try:
        subprocess.run(
            ['tar', '-czf', tar_path, '-C', pack_dir, '.'],
            check=True,
            cwd=PROJECT_ROOT,
        )
        size_mb = os.path.getsize(tar_path) / (1024 * 1024)
        print(f"  ✓ 打包完成: {tar_name} ({size_mb:.1f} MB)")
        return tar_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Windows用zip替代
        zip_name = f"comparison_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(PROJECT_ROOT, zip_name)
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', pack_dir)
        size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"  ✓ 打包完成(zip): {zip_name} ({size_mb:.1f} MB)")
        return zip_path


def main():
    parser = argparse.ArgumentParser(description='打包对比实验结果')
    parser.add_argument('--model', type=str, default='all',
                        choices=['all', 'v5', 'v12', 'v26', 'v13'],
                        help='指定要打包的模型 (默认: all)')
    args = parser.parse_args()

    print("=" * 60)
    print("  对比实验结果打包")
    print("=" * 60)
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if args.model == 'all':
        models = list(MODEL_MAP.keys())
        print(f"  打包范围: 全部模型")
    else:
        models = [args.model]
        print(f"  打包范围: {MODEL_MAP[args.model]['name']}")

    print("=" * 60)

    success_count = 0
    for key in models:
        if pack_model(key):
            success_count += 1

    if success_count > 0:
        pack_dir = os.path.join(PROJECT_ROOT, 'packed_results')
        tar_path = create_tar(pack_dir)
        print(f"\n  打包完成！请下载: {tar_path}")
    else:
        print(f"\n  ⚠ 没有可打包的结果")

    print("=" * 60)


if __name__ == '__main__':
    main()
