#!/bin/bash
# 克隆ARConv官方仓库并查看代码结构

cd /root/autodl-tmp/YOLOv11

# 克隆仓库（使用HTTPS，避免SSH密钥问题）
git clone https://github.com/WangXueyang-uestc/ARConv.git

# 进入目录
cd ARConv

# 显示目录结构
echo "=== ARConv 目录结构 ==="
find . -type f -name "*.py" | head -20

# 显示models目录内容
echo ""
echo "=== models 目录 ==="
ls -la models/

echo ""
echo "克隆完成！"
