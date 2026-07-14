#!/usr/bin/env python3
"""
修复ARConv以便在服务器上正常运行
1. 在tasks.py中添加ARConv导入
2. 验证修复
"""

import os
import sys

def fix_tasks_py():
    """在tasks.py中添加ARConv导入"""
    tasks_file = 'ultralytics/nn/tasks.py'
    
    if not os.path.exists(tasks_file):
        print(f"❌ 找不到文件: {tasks_file}")
        return False
    
    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'ARConv' in content:
        print("✅ ARConv已经在tasks.py中")
        return True
    
    # 在AConv后面添加ARConv
    content = content.replace('AConv,', 'AConv,\n    ARConv,')
    
    with open(tasks_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 验证
    with open(tasks_file, 'r', encoding='utf-8') as f:
        if 'ARConv' in f.read():
            print("✅ ARConv已成功添加到tasks.py")
            return True
        else:
            print("❌ ARConv添加失败")
            return False

def main():
    print("=" * 60)
    print("修复ARConv以便在服务器上运行")
    print("=" * 60)
    print()
    
    # 修复tasks.py
    print("1. 修复tasks.py...")
    if not fix_tasks_py():
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("✅ 所有修复完成！")
    print("=" * 60)
    print()
    print("下一步：")
    print("1. 运行 pack_complete_for_server.bat 重新打包")
    print("2. 上传到服务器并解压")
    print("3. 运行训练脚本")

if __name__ == '__main__':
    main()
