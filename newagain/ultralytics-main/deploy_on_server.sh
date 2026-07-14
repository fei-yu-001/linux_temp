#!/bin/bash
# ARConv消融实验 - 服务器部署脚本
# 在服务器上运行此脚本，自动复制所有文件到正确位置

echo "========================================"
echo "ARConv消融实验 - 服务器部署"
echo "========================================"
echo ""

# 设置颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查当前目录
if [ ! -f "run_arconv_ablation_experiments.py" ]; then
    echo -e "${RED}❌ 错误：请在 arconv_upload 目录中运行此脚本${NC}"
    echo "用法: cd /root/autodl-tmp/YOLOv11/arconv_upload && bash deploy_on_server.sh"
    exit 1
fi

# 设置目标目录
TARGET_DIR="/root/autodl-tmp/YOLOv11/ultralytics-main"

echo "目标目录: $TARGET_DIR"
echo ""

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ 错误：目标目录不存在: $TARGET_DIR${NC}"
    exit 1
fi

echo "开始复制文件..."
echo ""

# 1. 复制ARConv实现
echo "1. 复制ARConv实现..."
cp -v ultralytics/nn/modules/conv.py $TARGET_DIR/ultralytics/nn/modules/
cp -v ultralytics/nn/modules/__init__.py $TARGET_DIR/ultralytics/nn/modules/
echo -e "${GREEN}✅ ARConv实现已复制${NC}"
echo ""

# 2. 复制配置文件
echo "2. 复制配置文件..."
cp -v ultralytics/cfg/models/11/yolo11n_arconv_backbone.yaml $TARGET_DIR/ultralytics/cfg/models/11/
cp -v ultralytics/cfg/models/11/yolo11n_arconv_neck.yaml $TARGET_DIR/ultralytics/cfg/models/11/
cp -v ultralytics/cfg/models/11/yolo11n_arconv_head.yaml $TARGET_DIR/ultralytics/cfg/models/11/
cp -v ultralytics/cfg/models/11/yolo11n_arconv_full.yaml $TARGET_DIR/ultralytics/cfg/models/11/
echo -e "${GREEN}✅ 配置文件已复制${NC}"
echo ""

# 3. 复制训练脚本
echo "3. 复制训练脚本..."
cp -v arconv_callback.py $TARGET_DIR/
cp -v run_arconv_ablation_experiments.py $TARGET_DIR/
cp -v analyze_arconv_ablation.py $TARGET_DIR/
echo -e "${GREEN}✅ 训练脚本已复制${NC}"
echo ""

# 4. 复制文档（如果存在）
if [ -f "SERVER_DEPLOYMENT_CHECKLIST.md" ]; then
    echo "4. 复制部署文档..."
    cp -v SERVER_DEPLOYMENT_CHECKLIST.md $TARGET_DIR/
    cp -v FINAL_ABLATION_GUIDE.md $TARGET_DIR/ 2>/dev/null || true
    echo -e "${GREEN}✅ 部署文档已复制${NC}"
    echo ""
fi

echo "========================================"
echo -e "${GREEN}✅ 部署完成！${NC}"
echo "========================================"
echo ""

# 验证关键文件
echo "验证关键文件..."
echo ""

MISSING=0

# 检查ARConv实现
if [ -f "$TARGET_DIR/ultralytics/nn/modules/conv.py" ]; then
    echo -e "${GREEN}✅${NC} conv.py"
else
    echo -e "${RED}❌${NC} conv.py"
    MISSING=1
fi

# 检查配置文件
for config in backbone neck head full; do
    if [ -f "$TARGET_DIR/ultralytics/cfg/models/11/yolo11n_arconv_$config.yaml" ]; then
        echo -e "${GREEN}✅${NC} yolo11n_arconv_$config.yaml"
    else
        echo -e "${RED}❌${NC} yolo11n_arconv_$config.yaml"
        MISSING=1
    fi
done

# 检查训练脚本
if [ -f "$TARGET_DIR/run_arconv_ablation_experiments.py" ]; then
    echo -e "${GREEN}✅${NC} run_arconv_ablation_experiments.py"
else
    echo -e "${RED}❌${NC} run_arconv_ablation_experiments.py"
    MISSING=1
fi

echo ""

if [ $MISSING -eq 0 ]; then
    echo "========================================"
    echo -e "${GREEN}🎉 所有文件验证通过！${NC}"
    echo "========================================"
    echo ""
    echo "下一步："
    echo "1. cd $TARGET_DIR"
    echo "2. python run_arconv_ablation_experiments.py"
    echo ""
    echo "预计时间: 约4.8小时"
    echo "预计成本: 约¥10"
    echo ""
else
    echo "========================================"
    echo -e "${RED}⚠️  部分文件缺失，请检查！${NC}"
    echo "========================================"
    exit 1
fi
