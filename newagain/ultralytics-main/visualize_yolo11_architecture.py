#!/usr/bin/env python3
"""
YOLOv11 网络结构可视化脚本
生成类似YOLOv8风格的详细架构图
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形 - 增大画布
fig, ax = plt.subplots(1, 1, figsize=(24, 14))
ax.set_xlim(0, 24)
ax.set_ylim(-2, 24)
ax.axis('off')

# 定义颜色方案
colors = {
    'conv': '#A8D8EA',      # 浅蓝色 - Conv
    'c3k2': '#AA96DA',      # 紫色 - C3k2
    'sppf': '#FCBAD3',      # 粉色 - SPPF
    'c2psa': '#FFFFD2',     # 浅黄色 - C2PSA
    'upsample': '#A8E6CF',  # 浅绿色 - Upsample
    'concat': '#FFD3B6',    # 橙色 - Concat
    'detect': '#FF8B94',    # 红色 - Detect
}

def draw_module(ax, x, y, width, height, text, color, fontsize=10):
    """绘制模块方框"""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.1", 
        edgecolor='black', 
        facecolor=color,
        linewidth=2
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', 
            fontsize=fontsize, fontweight='bold')

def draw_arrow(ax, x1, y1, x2, y2, style='solid', color='black', width=2):
    """绘制箭头"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='->', 
        color=color,
        linewidth=width,
        linestyle=style,
        mutation_scale=20
    )
    ax.add_patch(arrow)

def draw_curved_arrow(ax, x1, y1, x2, y2, color='green', width=2):
    """绘制曲线箭头（用于跳跃连接）"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='->', 
        color=color,
        linewidth=width,
        connectionstyle="arc3,rad=0.3",
        mutation_scale=20
    )
    ax.add_patch(arrow)

# ============ Backbone 部分 ============
backbone_x = 3
y_start = 21

# 标题
ax.text(backbone_x, 22.5, 'Backbone', fontsize=16, fontweight='bold', 
        ha='center', bbox=dict(boxstyle='round', facecolor='lightgray'))

# Layer 0: Conv (P1/2)
draw_module(ax, backbone_x, y_start, 1.5, 0.7, '0: Conv\n64, 3, 2', colors['conv'], 8)
draw_arrow(ax, backbone_x, y_start-0.35, backbone_x, y_start-0.95)

# Layer 1: Conv (P2/4)
draw_module(ax, backbone_x, y_start-1.7, 1.5, 0.7, '1: Conv\n128, 3, 2', colors['conv'], 8)
draw_arrow(ax, backbone_x, y_start-2.05, backbone_x, y_start-2.65)

# Layer 2: C3k2
y_c3k2_1 = y_start-3.4
draw_module(ax, backbone_x, y_c3k2_1, 1.5, 0.7, '2: C3k2\n256', colors['c3k2'], 8)
draw_arrow(ax, backbone_x, y_c3k2_1-0.35, backbone_x, y_c3k2_1-0.95)

# Layer 3: Conv (P3/8)
draw_module(ax, backbone_x, y_start-5.1, 1.5, 0.7, '3: Conv\n256, 3, 2', colors['conv'], 8)
draw_arrow(ax, backbone_x, y_start-5.45, backbone_x, y_start-6.05)

# Layer 4: C3k2 (P3)
y_p3 = y_start-6.8
draw_module(ax, backbone_x, y_p3, 1.5, 0.7, '4: C3k2\n512', colors['c3k2'], 8)
draw_arrow(ax, backbone_x, y_p3-0.35, backbone_x, y_p3-0.95)

# Layer 5: Conv (P4/16)
draw_module(ax, backbone_x, y_start-8.5, 1.5, 0.7, '5: Conv\n512, 3, 2', colors['conv'], 8)
draw_arrow(ax, backbone_x, y_start-8.85, backbone_x, y_start-9.45)

# Layer 6: C3k2 (P4)
y_p4 = y_start-10.2
draw_module(ax, backbone_x, y_p4, 1.5, 0.7, '6: C3k2\n512', colors['c3k2'], 8)
draw_arrow(ax, backbone_x, y_p4-0.35, backbone_x, y_p4-0.95)

# Layer 7: Conv (P5/32)
draw_module(ax, backbone_x, y_start-11.9, 1.5, 0.7, '7: Conv\n1024, 3, 2', colors['conv'], 8)
draw_arrow(ax, backbone_x, y_start-12.25, backbone_x, y_start-12.85)

# Layer 8: C3k2
draw_module(ax, backbone_x, y_start-13.6, 1.5, 0.7, '8: C3k2\n1024', colors['c3k2'], 8)
draw_arrow(ax, backbone_x, y_start-13.95, backbone_x, y_start-14.55)

# Layer 9: SPPF
draw_module(ax, backbone_x, y_start-15.3, 1.5, 0.7, '9: SPPF\n1024', colors['sppf'], 8)
draw_arrow(ax, backbone_x, y_start-15.65, backbone_x, y_start-16.25)

# Layer 10: C2PSA (P5)
y_p5 = y_start-17
draw_module(ax, backbone_x, y_p5, 1.5, 0.7, '10: C2PSA\n1024', colors['c2psa'], 8)

# ============ Neck 部分 ============
neck_x = 12
ax.text(neck_x, 22.5, 'Neck', fontsize=16, fontweight='bold', 
        ha='center', bbox=dict(boxstyle='round', facecolor='lightgray'))

# Layer 11: Upsample
y_up1 = y_p5
draw_module(ax, neck_x-4, y_up1, 1.5, 0.7, '11: Up\n×2', colors['upsample'], 8)
draw_arrow(ax, backbone_x+0.75, y_p5, neck_x-4.75, y_up1)

# Layer 12: Concat (P4)
y_concat1 = y_p5+1.7
draw_module(ax, neck_x-4, y_concat1, 1.5, 0.7, '12: Concat', colors['concat'], 8)
draw_arrow(ax, neck_x-4, y_up1+0.35, neck_x-4, y_concat1-0.35)
# 从P4跳跃连接
draw_curved_arrow(ax, backbone_x+0.75, y_p4, neck_x-4.75, y_concat1-0.2, 'green', 2)

# Layer 13: C3k2
y_neck_p4 = y_concat1+1.7
draw_module(ax, neck_x-4, y_neck_p4, 1.5, 0.7, '13: C3k2\n512', colors['c3k2'], 8)
draw_arrow(ax, neck_x-4, y_concat1+0.35, neck_x-4, y_neck_p4-0.35)

# Layer 14: Upsample
y_up2 = y_neck_p4+1.7
draw_module(ax, neck_x-4, y_up2, 1.5, 0.7, '14: Up\n×2', colors['upsample'], 8)
draw_arrow(ax, neck_x-4, y_neck_p4+0.35, neck_x-4, y_up2-0.35)

# Layer 15: Concat (P3)
y_concat2 = y_up2+1.7
draw_module(ax, neck_x-4, y_concat2, 1.5, 0.7, '15: Concat', colors['concat'], 8)
draw_arrow(ax, neck_x-4, y_up2+0.35, neck_x-4, y_concat2-0.35)
# 从P3跳跃连接
draw_curved_arrow(ax, backbone_x+0.75, y_p3, neck_x-4.75, y_concat2-0.2, 'green', 2)

# Layer 16: C3k2 (P3/8-small)
y_out_p3 = y_concat2+1.7
draw_module(ax, neck_x-4, y_out_p3, 1.5, 0.7, '16: C3k2\n256\n(P3/8)', colors['c3k2'], 8)
draw_arrow(ax, neck_x-4, y_concat2+0.35, neck_x-4, y_out_p3-0.35)

# Layer 17: Conv (downsample)
y_down1 = y_out_p3-1.7
draw_module(ax, neck_x, y_down1, 1.5, 0.7, '17: Conv\n256, 3, 2', colors['conv'], 8)
draw_arrow(ax, neck_x-4, y_out_p3-0.35, neck_x-0.75, y_down1+0.2)

# Layer 18: Concat
y_concat3 = y_down1-1.7
draw_module(ax, neck_x, y_concat3, 1.5, 0.7, '18: Concat', colors['concat'], 8)
draw_arrow(ax, neck_x, y_down1-0.35, neck_x, y_concat3+0.35)
# 从layer 13跳跃连接
draw_curved_arrow(ax, neck_x-3.25, y_neck_p4, neck_x-0.75, y_concat3+0.2, 'green', 2)

# Layer 19: C3k2 (P4/16-medium)
y_out_p4 = y_concat3-1.7
draw_module(ax, neck_x, y_out_p4, 1.5, 0.7, '19: C3k2\n512\n(P4/16)', colors['c3k2'], 8)
draw_arrow(ax, neck_x, y_concat3-0.35, neck_x, y_out_p4+0.35)

# Layer 20: Conv (downsample)
y_down2 = y_out_p4-1.7
draw_module(ax, neck_x+4, y_down2, 1.5, 0.7, '20: Conv\n512, 3, 2', colors['conv'], 8)
draw_arrow(ax, neck_x, y_out_p4-0.35, neck_x+3.25, y_down2+0.2)

# Layer 21: Concat
y_concat4 = y_down2-1.7
draw_module(ax, neck_x+4, y_concat4, 1.5, 0.7, '21: Concat', colors['concat'], 8)
draw_arrow(ax, neck_x+4, y_down2-0.35, neck_x+4, y_concat4+0.35)
# 从layer 10跳跃连接
draw_curved_arrow(ax, backbone_x+0.75, y_p5+0.2, neck_x+3.25, y_concat4+0.2, 'green', 2)

# Layer 22: C3k2 (P5/32-large)
y_out_p5 = y_concat4-1.7
draw_module(ax, neck_x+4, y_out_p5, 1.5, 0.7, '22: C3k2\n1024\n(P5/32)', colors['c3k2'], 8)
draw_arrow(ax, neck_x+4, y_concat4-0.35, neck_x+4, y_out_p5+0.35)

# ============ Head 部分 ============
head_x = 20
ax.text(head_x, 22.5, 'Head', fontsize=16, fontweight='bold', 
        ha='center', bbox=dict(boxstyle='round', facecolor='lightgray'))

# Layer 23: Detect
y_detect_p3 = y_out_p3
y_detect_p4 = y_out_p4
y_detect_p5 = y_out_p5

draw_module(ax, head_x, y_detect_p3, 1.8, 0.7, '23: Detect\n(P3)', colors['detect'], 8)
draw_module(ax, head_x, y_detect_p4, 1.8, 0.7, '23: Detect\n(P4)', colors['detect'], 8)
draw_module(ax, head_x, y_detect_p5, 1.8, 0.7, '23: Detect\n(P5)', colors['detect'], 8)

# 连接到Detect
draw_arrow(ax, neck_x-3.25, y_out_p3, head_x-0.9, y_detect_p3)
draw_arrow(ax, neck_x+0.75, y_out_p4, head_x-0.9, y_detect_p4)
draw_arrow(ax, neck_x+4.75, y_out_p5, head_x-0.9, y_detect_p5)

# 添加图例
legend_x = 1.5
legend_y = 3
ax.text(legend_x, legend_y+1.5, 'Legend:', fontsize=12, fontweight='bold')

legend_items = [
    ('Conv', colors['conv']),
    ('C3k2', colors['c3k2']),
    ('SPPF', colors['sppf']),
    ('C2PSA', colors['c2psa']),
    ('Upsample', colors['upsample']),
    ('Concat', colors['concat']),
    ('Detect', colors['detect']),
]

for i, (name, color) in enumerate(legend_items):
    y_pos = legend_y - i*0.6
    draw_module(ax, legend_x+1, y_pos, 1, 0.4, name, color, 9)

# 添加标题
fig.suptitle('YOLOv11 Network Architecture (Detailed View)', 
             fontsize=22, fontweight='bold', y=0.98)

# 添加说明
ax.text(12, 0, 'Green arrows: Skip connections | Black arrows: Forward flow', 
        fontsize=11, ha='center', style='italic',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('yolo11_architecture_detailed.png', dpi=300, bbox_inches='tight')
print("✅ YOLOv11架构图已保存为: yolo11_architecture_detailed.png")
plt.show()
