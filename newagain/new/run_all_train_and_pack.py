#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键训练 + 自动打包脚本
功能：依次训练4个补充模型，训练完成后自动打包结果

使用方法：
    python run_all_train_and_pack.py

统一超参: epochs=150, batch=16, imgsz=640, cache=True,
          close_mosaic=10, workers=8, optimizer=SGD, amp=True, device='0'
"""
import subprocess
import time
import os
import shutil
from datetime import datetime

# ============================================================
# 配置区
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# AutoDL上的项目根目录（训练时用）
REMOTE_ROOT = '/root/autodl-tmp/YOLOv11/new'

# 实验配置：按顺序执行
EXPERIMENTS = [
    {
        'script': 'train_yolov5n_domestic.py',
        'model': 'YOLOv5n',
        'cwd': os.path.join(PROJECT_ROOT, 'ultralytics-latest'),
        'result_dir': 'ultralytics-latest/runs/train/yolov5n_domestic',
    },
    {
        'script': 'train_yolo12n_domestic.py',
        'model': 'YOLO12n',
        'cwd': os.path.join(PROJECT_ROOT, 'ultralytics-latest'),
        'result_dir': 'ultralytics-latest/runs/train/yolo12n_domestic',
    },
    {
        'script': 'train_yolo26n_domestic.py',
        'model': 'YOLO26n',
        'cwd': os.path.join(PROJECT_ROOT, 'ultralytics-latest'),
        'result_dir': 'ultralytics-latest/runs/train/yolo26n_domestic',
    },
    {
        'script': 'train_yolov13n_domestic.py',
        'model': 'YOLOv13n',
        'cwd': os.path.join(PROJECT_ROOT, 'yolov13'),
        'result_dir': 'yolov13/runs/train/yolov13n_domestic',
    },
]


# ============================================================
# 训练函数
# ============================================================
def run_training(script_name, model_name, cwd):
    """运行单个训练脚本"""
    print(f"\n{'='*60}")
    print(f"  开始训练: {model_name}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  工作目录: {cwd}")
    print(f"  脚本: {script_name}")
    print(f"{'='*60}\n")

    start_time = time.time()

    try:
        result = subprocess.run(
            ['python', script_name],
            check=True,
            capture_output=False,
            cwd=cwd,
        )

        elapsed = time.time() - start_time
        h = int(elapsed // 3600)
        m = int((elapsed % 3600) // 60)
        s = int(elapsed % 60)

        print(f"\n  ✓ {model_name} 训练完成！用时: {h}时{m}分{s}秒")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n  ✗ {model_name} 训练失败！错误: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n  ⚠ 用户中断训练: {model_name}")
        raise


# ============================================================
# 打包函数
# ============================================================
def pack_results(results_dict):
    """训练完成后打包所有结果"""
    print(f"\n{'='*60}")
    print(f"  开始打包实验结果")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    pack_dir = os.path.join(PROJECT_ROOT, 'packed_results')
    os.makedirs(pack_dir, exist_ok=True)

    # 收集每个模型的关键文件
    key_files = ['weights/best.pt', 'weights/last.pt', 'results.csv', 'results.png',
                 'confusion_matrix.png', 'labels.jpg', 'PR_curve.png', 'F1_curve.png']

    summary_lines = []
    summary_lines.append(f"对比实验结果汇总 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    summary_lines.append("=" * 60)
    summary_lines.append(f"统一超参: epochs=150, batch=16, imgsz=640, optimizer=SGD")
    summary_lines.append("")

    for model_name, success in results_dict.items():
        status = "成功" if success else "失败"
        summary_lines.append(f"{model_name}: {status}")

        # 找到对应的result_dir
        result_dir = None
        for exp in EXPERIMENTS:
            if exp['model'] == model_name:
                result_dir = os.path.join(PROJECT_ROOT, exp['result_dir'])
                break

        if not success or not result_dir or not os.path.isdir(result_dir):
            continue

        # 复制关键文件到打包目录
        model_pack_dir = os.path.join(pack_dir, model_name)
        os.makedirs(model_pack_dir, exist_ok=True)

        for f in key_files:
            src = os.path.join(result_dir, f)
            if os.path.isfile(src):
                dst = os.path.join(model_pack_dir, os.path.basename(f))
                shutil.copy2(src, dst)
                print(f"  复制: {model_name}/{os.path.basename(f)}")

        # 读取mAP结果
        csv_path = os.path.join(result_dir, 'results.csv')
        if os.path.isfile(csv_path):
            try:
                with open(csv_path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 1:
                        last_line = lines[-1].strip()
                        vals = last_line.split(',')
                        # ultralytics results.csv格式：epoch, train/box_loss, ..., metrics/mAP50(B), metrics/mAP50-95(B), ...
                        # 取最后几个关键指标
                        summary_lines.append(f"  最后epoch数据: {last_line[:120]}")
            except Exception as e:
                summary_lines.append(f"  读取results.csv失败: {e}")

    # 写入汇总文件
    summary_path = os.path.join(pack_dir, 'summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_lines))
    print(f"\n  汇总文件: {summary_path}")

    # tar打包
    tar_name = f"comparison_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
    tar_path = os.path.join(PROJECT_ROOT, tar_name)

    print(f"\n  正在打包: {tar_name} ...")
    try:
        subprocess.run(
            ['tar', '-czf', tar_path, '-C', pack_dir, '.'],
            check=True,
            cwd=PROJECT_ROOT,
        )
        size_mb = os.path.getsize(tar_path) / (1024 * 1024)
        print(f"  ✓ 打包完成: {tar_name} ({size_mb:.1f} MB)")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Windows可能没有tar，用zip替代
        zip_name = f"comparison_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(PROJECT_ROOT, zip_name)
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', pack_dir)
        size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"  ✓ 打包完成(zip): {zip_name} ({size_mb:.1f} MB)")

    print(f"\n  打包目录: {pack_dir}")
    print(f"  可直接下载到本地查看结果")


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 60)
    print("  YOLO对比实验 · 一键训练+打包")
    print("=" * 60)
    print(f"  数据集: domestic_dataset (31类昆虫)")
    print(f"  训练参数: epochs=150, batch=16, imgsz=640, optimizer=SGD")
    print(f"  模型数量: {len(EXPERIMENTS)}")
    print(f"    ultralytics-latest: YOLOv5n → YOLO12n → YOLO26n")
    print(f"    yolov13: YOLOv13n")
    print(f"  开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    total_start = time.time()
    results = {}

    # 依次训练
    for i, exp in enumerate(EXPERIMENTS):
        print(f"\n>>> 进度: [{i+1}/{len(EXPERIMENTS)}] <<<")
        success = run_training(exp['script'], exp['model'], exp['cwd'])
        results[exp['model']] = success

        if not success:
            print(f"\n  ⚠ {exp['model']} 训练失败，继续下一个模型...")

    # 训练总结
    total_elapsed = time.time() - total_start
    h = int(total_elapsed // 3600)
    m = int((total_elapsed % 3600) // 60)

    print(f"\n{'='*60}")
    print(f"  训练完成总结")
    print(f"{'='*60}")
    print(f"  总用时: {h}时{m}分")
    print(f"  完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n  训练结果:")
    success_count = 0
    for model_name, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        print(f"    {model_name}: {status}")
        if success:
            success_count += 1

    print(f"\n  成功: {success_count}/{len(EXPERIMENTS)}")

    # 自动打包
    if success_count > 0:
        print(f"\n>>> 开始自动打包 <<<")
        pack_results(results)
    else:
        print(f"\n  ⚠ 无成功训练结果，跳过打包")

    # 最终输出
    print(f"\n{'='*60}")
    print(f"  全部流程结束")
    print(f"{'='*60}")
    print(f"  结果位置:")
    for exp in EXPERIMENTS:
        print(f"    {exp['model']}: {exp['result_dir']}/")
    print(f"  打包文件: comparison_results_*.tar.gz")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
