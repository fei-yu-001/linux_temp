#!/bin/bash
# 从官方仓库获取ARConv代码并集成到Ultralytics

set -e  # 遇到错误立即退出

echo "========================================================================"
echo "从官方仓库获取ARConv代码"
echo "========================================================================"

cd /root/autodl-tmp/YOLOv11

# 步骤1: 克隆官方仓库
echo ""
echo "步骤1: 克隆ARConv官方仓库..."
if [ -d "ARConv" ]; then
    echo "  ARConv目录已存在，跳过克隆"
else
    git clone https://github.com/WangXueyang-uestc/ARConv.git
    echo "  ✓ 克隆完成"
fi

# 步骤2: 查看目录结构
echo ""
echo "步骤2: 查看ARConv目录结构..."
cd ARConv
echo "  目录内容:"
ls -la
echo ""
echo "  Python文件:"
find . -name "*.py" -type f

# 步骤3: 提取ARConv代码
echo ""
echo "步骤3: 提取ARConv核心代码..."
cd /root/autodl-tmp/YOLOv11/ultralytics-main
python3 extract_arconv_code.py

echo ""
echo "========================================================================"
echo "完成！请查看 arconv_official.py 文件"
echo "========================================================================"
