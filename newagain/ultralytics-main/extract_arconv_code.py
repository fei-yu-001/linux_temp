#!/usr/bin/env python3
"""
从官方ARConv仓库提取核心代码
"""

import os
import shutil

def extract_arconv():
    """提取ARConv核心实现"""
    
    arconv_repo = "/root/autodl-tmp/YOLOv11/ARConv"
    
    if not os.path.exists(arconv_repo):
        print("错误: ARConv仓库不存在")
        print("请先运行: bash clone_arconv.sh")
        return
    
    print("="*70)
    print("提取ARConv核心代码")
    print("="*70)
    
    # 查找所有Python文件
    print("\n1. 查找Python文件...")
    for root, dirs, files in os.walk(arconv_repo):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, arconv_repo)
                print(f"  - {rel_path}")
    
    # 读取ARConv.py
    arconv_file = os.path.join(arconv_repo, "models", "ARConv.py")
    if os.path.exists(arconv_file):
        print(f"\n2. 读取 {arconv_file}")
        print("-"*70)
        with open(arconv_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        print("-"*70)
        
        # 保存到当前目录
        output_file = "arconv_official.py"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ 已保存到: {output_file}")
    else:
        print(f"\n✗ 找不到文件: {arconv_file}")
    
    # 查找其他相关文件
    print("\n3. 查找其他相关文件...")
    important_files = [
        "models/__init__.py",
        "models/base_model.py",
        "models/common.py",
        "utils/model_utils.py",
    ]
    
    for file_path in important_files:
        full_path = os.path.join(arconv_repo, file_path)
        if os.path.exists(full_path):
            print(f"  ✓ 找到: {file_path}")
            # 读取并显示前50行
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:50]
                print(f"\n--- {file_path} (前50行) ---")
                print(''.join(lines))
        else:
            print(f"  ✗ 未找到: {file_path}")
    
    print("\n" + "="*70)
    print("提取完成！")
    print("="*70)

if __name__ == '__main__':
    extract_arconv()
