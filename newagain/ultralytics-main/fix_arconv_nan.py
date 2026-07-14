#!/usr/bin/env python3
"""
修复ARConv的NaN问题
主要修复：
1. 移除 x * 100 操作（导致数值爆炸）
2. 简化 p_conv 结构
3. 添加数值稳定性保护
"""

import re

def fix_arconv():
    """修复ARConv实现中的NaN问题"""
    
    conv_file = 'ultralytics/nn/modules/conv.py'
    
    print("🔧 开始修复ARConv...")
    
    with open(conv_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到ARConv类的forward方法
    # 修复1: 移除 x * 100 操作
    content = re.sub(
        r'offset = self\.p_conv\(x \* 100\)',
        'offset = self.p_conv(x)',
        content
    )
    
    # 修复2: 简化p_conv结构（在__init__中）
    # 将2层卷积简化为1层
    old_p_conv = r'''self\.p_conv = nn\.Sequential\(
            nn\.Conv2d\(c1, c1, 3, 1, 1\),
            nn\.BatchNorm2d\(c1\),
            nn\.LeakyReLU\(inplace=True\),
            nn\.Conv2d\(c1, c1, 3, 1, 1\),
            nn\.BatchNorm2d\(c1\),
            nn\.LeakyReLU\(inplace=True\)
        \)'''
    
    new_p_conv = '''self.p_conv = nn.Sequential(
            nn.Conv2d(c1, c1, 3, 1, 1),
            nn.BatchNorm2d(c1),
            nn.LeakyReLU(inplace=True)
        )'''
    
    content = re.sub(old_p_conv, new_p_conv, content, flags=re.MULTILINE)
    
    # 修复3: 在forward中添加数值裁剪，防止梯度爆炸
    # 在 l = l * (self.hw_range[1] - 1) + 1 之后添加clamp
    content = re.sub(
        r'(l = l \* \(self\.hw_range\[1\] - 1\) \+ 1)\n',
        r'\1\n        l = torch.clamp(l, 1.0, self.hw_range[1])  # 防止数值爆炸\n',
        content
    )
    
    content = re.sub(
        r'(w = w \* \(self\.hw_range\[1\] - 1\) \+ 1)\n',
        r'\1\n        w = torch.clamp(w, 1.0, self.hw_range[1])  # 防止数值爆炸\n',
        content
    )
    
    # 修复4: 在forward_fuse中也做同样的修复
    content = re.sub(
        r'offset = self\.p_conv\(x \* 100\)',
        'offset = self.p_conv(x)',
        content
    )
    
    # 在forward_fuse中也添加clamp
    # 找到forward_fuse方法中的l和w计算
    lines = content.split('\n')
    new_lines = []
    in_forward_fuse = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        if 'def forward_fuse(self, x):' in line:
            in_forward_fuse = True
        elif in_forward_fuse and 'def ' in line and 'forward_fuse' not in line:
            in_forward_fuse = False
        
        # 在forward_fuse中的l和w计算后添加clamp
        if in_forward_fuse:
            if 'l = l * (self.hw_range[1] - 1) + 1' in line and 'clamp' not in lines[i+1] if i+1 < len(lines) else True:
                new_lines.append('        l = torch.clamp(l, 1.0, self.hw_range[1])  # 防止数值爆炸')
            elif 'w = w * (self.hw_range[1] - 1) + 1' in line and 'clamp' not in lines[i+1] if i+1 < len(lines) else True:
                new_lines.append('        w = torch.clamp(w, 1.0, self.hw_range[1])  # 防止数值爆炸')
    
    content = '\n'.join(new_lines)
    
    # 保存修复后的文件
    with open(conv_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ ARConv修复完成！")
    print("\n修复内容：")
    print("  1. 移除 x * 100 操作（防止数值爆炸）")
    print("  2. 简化 p_conv 为单层卷积（提升速度）")
    print("  3. 添加 torch.clamp 防止梯度爆炸")
    print("\n现在可以重新运行训练了！")

if __name__ == '__main__':
    fix_arconv()
