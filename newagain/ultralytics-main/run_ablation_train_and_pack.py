#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消融实验一键训练+打包脚本
7个实验顺序执行，训练完成后自动打包

实验矩阵:
  #0 Baseline   — 无ARConv
  #1 ARConv-1L  — Backbone P5/32 (1层)
  #2 ARConv-2L  — Backbone P4+P5 (2层)
  #3 ARConv-3L  — Backbone P3+P4+P5 (3层)
  #4 ARConv-Neck— Neck PAN下采样 (2层, 位置维度)
  #5 ARConv-BB  — Backbone全部 (5层)
  #6 ARConv-Full— Backbone+Head全部 (7层)

统一超参: epochs=150, batch=16, imgsz=640, cache=True,
          close_mosaic=10, workers=8, optimizer=SGD, amp=True, device='0'
"""
import subprocess
import time
import os
import shutil
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ABLATION_DIR = os.path.join(PROJECT_ROOT, 'ablation')

EXPERIMENTS = [
    {'script': 'train_ablation_baseline.py',  'name': 'Baseline',    'layers': 0, 'rdir': 'runs/ablation/baseline'},
    {'script': 'train_ablation_1layer.py',    'name': 'ARConv-1L',   'layers': 1, 'rdir': 'runs/ablation/arconv_1layer'},
    {'script': 'train_ablation_2layers.py',   'name': 'ARConv-2L',   'layers': 2, 'rdir': 'runs/ablation/arconv_2layers'},
    {'script': 'train_ablation_3layers.py',   'name': 'ARConv-3L',   'layers': 3, 'rdir': 'runs/ablation/arconv_3layers'},
    {'script': 'train_ablation_neck.py',      'name': 'ARConv-Neck', 'layers': 2, 'rdir': 'runs/ablation/arconv_neck'},
    {'script': 'train_ablation_backbone.py',  'name': 'ARConv-BB',   'layers': 5, 'rdir': 'runs/ablation/arconv_backbone'},
    {'script': 'train_ablation_full.py',      'name': 'ARConv-Full', 'layers': 7, 'rdir': 'runs/ablation/arconv_full'},
]

KEY_FILES = ['weights/best.pt', 'weights/last.pt', 'results.csv', 'results.png',
             'confusion_matrix.png', 'args.yaml']


def run_training(script_name, exp_name, cwd):
    print(f"\n{'='*60}")
    print(f"  开始训练: {exp_name}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    start = time.time()
    try:
        subprocess.run(['python', script_name], check=True, cwd=cwd)
        elapsed = time.time() - start
        h, m, s = int(elapsed//3600), int((elapsed%3600)//60), int(elapsed%60)
        print(f"\n  OK {exp_name} 用时: {h}h{m}m{s}s")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n  FAIL {exp_name}: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n  中断: {exp_name}")
        raise


def pack_results(results):
    print(f"\n{'='*60}\n  打包结果\n{'='*60}\n")
    pack_dir = os.path.join(PROJECT_ROOT, 'ablation_packed')
    os.makedirs(pack_dir, exist_ok=True)

    for exp in EXPERIMENTS:
        name = exp['name']
        if not results.get(name):
            continue
        rdir = os.path.join(PROJECT_ROOT, exp['rdir'])
        if not os.path.isdir(rdir):
            continue
        dst = os.path.join(pack_dir, name)
        os.makedirs(dst, exist_ok=True)
        for f in KEY_FILES:
            src = os.path.join(rdir, f)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(dst, os.path.basename(f)))

    # 汇总
    summary = [f"ARConv消融实验 {datetime.now().strftime('%Y%m%d %H:%M')}"]
    summary.append("超参: epochs=150, batch=16, imgsz=640, optimizer=SGD")
    summary.append(f"{'实验':<15} {'ARConv':<8} {'状态'}")
    for exp in EXPERIMENTS:
        s = "OK" if results.get(exp['name']) else "FAIL"
        summary.append(f"{exp['name']:<15} {exp['layers']:<8} {s}")

    with open(os.path.join(pack_dir, 'summary.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary))

    # 压缩
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    try:
        tar = f"ablation_{ts}.tar.gz"
        subprocess.run(['tar', '-czf', tar, '-C', pack_dir, '.'], check=True, cwd=PROJECT_ROOT)
        print(f"  打包: {tar} ({os.path.getsize(os.path.join(PROJECT_ROOT,tar))/1e6:.1f}MB)")
    except Exception:
        zipn = f"ablation_{ts}.zip"
        shutil.make_archive(os.path.join(PROJECT_ROOT, zipn.replace('.zip','')), 'zip', pack_dir)
        print(f"  打包: {zipn}")


def main():
    print("=" * 60)
    print("  ARConv消融实验 · 一键训练+打包")
    print("=" * 60)
    print(f"  实验: {len(EXPERIMENTS)}个")
    print(f"  超参: epochs=150, batch=16, imgsz=640, SGD")
    print(f"\n  #  {'实验名':<15} {'ARConv层':<8} 维度")
    print(f"  {'-'*40}")
    dims = ['基线','深度','深度','深度','位置','深度','位置']
    for i, exp in enumerate(EXPERIMENTS):
        print(f"  {i}  {exp['name']:<15} {exp['layers']:<8} {dims[i]}")
    print("=" * 60)

    results = {}
    for i, exp in enumerate(EXPERIMENTS):
        print(f"\n>>> [{i+1}/{len(EXPERIMENTS)}] <<<")
        results[exp['name']] = run_training(exp['script'], exp['name'], ABLATION_DIR)

    ok = sum(1 for v in results.values() if v)
    print(f"\n  完成: {ok}/{len(EXPERIMENTS)}")
    for name, s in results.items():
        print(f"    {'OK' if s else 'FAIL'} {name}")

    if ok > 0:
        pack_results(results)


if __name__ == '__main__':
    main()
