#!/bin/bash
# ARConv消融实验 - 服务器快速部署脚本
# 用于解压完整的ultralytics-main压缩包并验证

echo "========================================"
echo "ARConv消融实验 - 快速部署"
echo "========================================"
echo ""

# 设置颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 工作目录
WORK_DIR="/root/autodl-tmp/YOLOv11"
ZIP_FILE="ultralytics-main-complete.zip"

echo -e "${BLUE}📂 工作目录: $WORK_DIR${NC}"
echo ""

# 检查是否在正确的目录
if [ ! -d "$WORK_DIR" ]; then
    echo -e "${RED}❌ 错误：工作目录不存在: $WORK_DIR${NC}"
    echo "请先创建目录: mkdir -p $WORK_DIR"
    exit 1
fi

cd $WORK_DIR

# 检查压缩包是否存在
if [ ! -f "$ZIP_FILE" ]; then
    echo -e "${RED}❌ 错误：未找到压缩包: $ZIP_FILE${NC}"
    echo ""
    echo "请先上传压缩包到: $WORK_DIR/"
    echo ""
    echo "上传方法："
    echo "1. 使用MobaXterm连接到服务器"
    echo "2. 在左侧文件浏览器中导航到 $WORK_DIR/"
    echo "3. 将本地的 $ZIP_FILE 拖拽到服务器"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ 找到压缩包: $ZIP_FILE${NC}"
echo ""

# 显示压缩包大小
SIZE=$(du -h "$ZIP_FILE" | cut -f1)
echo "压缩包大小: $SIZE"
echo ""

# 备份旧版本（如果存在）
if [ -d "ultralytics-main" ]; then
    BACKUP_NAME="ultralytics-main-backup-$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}⚠️  检测到旧版本，正在备份...${NC}"
    mv ultralytics-main "$BACKUP_NAME"
    echo -e "${GREEN}✅ 已备份到: $BACKUP_NAME${NC}"
    echo ""
fi

# 解压文件
echo "📦 正在解压..."
unzip -q "$ZIP_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 解压完成！${NC}"
    echo ""
else
    echo -e "${RED}❌ 解压失败！${NC}"
    exit 1
fi

# 验证关键文件
echo "========================================"
echo "🔍 验证关键文件"
echo "========================================"
echo ""

cd ultralytics-main

MISSING=0

# 检查ARConv实现
echo "检查ARConv实现..."
if [ -f "ultralytics/nn/modules/conv.py" ]; then
    # 检查是否包含ARConv类
    if grep -q "class ARConv" ultralytics/nn/modules/conv.py; then
        echo -e "${GREEN}✅${NC} conv.py (包含ARConv类)"
    else
        echo -e "${YELLOW}⚠️${NC} conv.py (未找到ARConv类)"
        MISSING=1
    fi
else
    echo -e "${RED}❌${NC} conv.py"
    MISSING=1
fi

if [ -f "ultralytics/nn/modules/__init__.py" ]; then
    # 检查是否导入了ARConv
    if grep -q "ARConv" ultralytics/nn/modules/__init__.py; then
        echo -e "${GREEN}✅${NC} __init__.py (已导入ARConv)"
    else
        echo -e "${YELLOW}⚠️${NC} __init__.py (未导入ARConv)"
        MISSING=1
    fi
else
    echo -e "${RED}❌${NC} __init__.py"
    MISSING=1
fi

echo ""

# 检查配置文件
echo "检查配置文件..."
for config in backbone neck head full; do
    if [ -f "ultralytics/cfg/models/11/yolo11n_arconv_$config.yaml" ]; then
        echo -e "${GREEN}✅${NC} yolo11n_arconv_$config.yaml"
    else
        echo -e "${RED}❌${NC} yolo11n_arconv_$config.yaml"
        MISSING=1
    fi
done

echo ""

# 检查训练脚本
echo "检查训练脚本..."
if [ -f "arconv_callback.py" ]; then
    echo -e "${GREEN}✅${NC} arconv_callback.py"
else
    echo -e "${RED}❌${NC} arconv_callback.py"
    MISSING=1
fi

if [ -f "run_arconv_ablation_experiments.py" ]; then
    echo -e "${GREEN}✅${NC} run_arconv_ablation_experiments.py"
else
    echo -e "${RED}❌${NC} run_arconv_ablation_experiments.py"
    MISSING=1
fi

if [ -f "analyze_arconv_ablation.py" ]; then
    echo -e "${GREEN}✅${NC} analyze_arconv_ablation.py"
else
    echo -e "${RED}❌${NC} analyze_arconv_ablation.py"
    MISSING=1
fi

echo ""

# 检查数据集
echo "检查数据集..."
if [ -f "/root/autodl-tmp/domestic_dataset/data.yaml" ]; then
    echo -e "${GREEN}✅${NC} 数据集配置文件存在"
    
    # 显示数据集信息
    NC=$(grep "^nc:" /root/autodl-tmp/domestic_dataset/data.yaml | awk '{print $2}')
    if [ ! -z "$NC" ]; then
        echo "   类别数: $NC"
    fi
else
    echo -e "${RED}❌${NC} 数据集配置文件不存在"
    echo "   预期路径: /root/autodl-tmp/domestic_dataset/data.yaml"
    MISSING=1
fi

echo ""

# 检查Python环境
echo "检查Python环境..."
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo -e "${GREEN}✅${NC} Python: $PYTHON_VERSION"
    
    # 检查ultralytics
    if python -c "import ultralytics" 2>/dev/null; then
        ULTRALYTICS_VERSION=$(python -c "import ultralytics; print(ultralytics.__version__)" 2>/dev/null)
        echo -e "${GREEN}✅${NC} ultralytics: $ULTRALYTICS_VERSION"
    else
        echo -e "${YELLOW}⚠️${NC} ultralytics未安装"
        echo "   运行: pip install ultralytics"
    fi
    
    # 检查其他依赖
    for pkg in pandas matplotlib seaborn; do
        if python -c "import $pkg" 2>/dev/null; then
            echo -e "${GREEN}✅${NC} $pkg"
        else
            echo -e "${YELLOW}⚠️${NC} $pkg未安装"
        fi
    done
else
    echo -e "${RED}❌${NC} Python未安装"
    MISSING=1
fi

echo ""

# 检查GPU
echo "检查GPU..."
if command -v nvidia-smi &> /dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -n 1)
    GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader | head -n 1)
    echo -e "${GREEN}✅${NC} GPU: $GPU_NAME"
    echo "   显存: $GPU_MEM"
else
    echo -e "${RED}❌${NC} nvidia-smi不可用"
    MISSING=1
fi

echo ""

# 检查磁盘空间
echo "检查磁盘空间..."
DISK_AVAIL=$(df -h /root/autodl-tmp/ | tail -n 1 | awk '{print $4}')
echo "可用空间: $DISK_AVAIL"

# 转换为GB进行比较
DISK_AVAIL_GB=$(df -BG /root/autodl-tmp/ | tail -n 1 | awk '{print $4}' | sed 's/G//')
if [ "$DISK_AVAIL_GB" -lt 50 ]; then
    echo -e "${YELLOW}⚠️  警告：磁盘空间不足50GB，可能影响训练${NC}"
else
    echo -e "${GREEN}✅${NC} 磁盘空间充足"
fi

echo ""

# 总结
echo "========================================"
if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}🎉 所有检查通过！${NC}"
    echo "========================================"
    echo ""
    echo -e "${BLUE}📋 实验配置${NC}"
    echo "  实验数量: 4个"
    echo "  实验列表:"
    echo "    1. ARConv Backbone替换（5层）"
    echo "    2. ARConv Neck替换（2层）"
    echo "    3. ARConv Head替换（2层）"
    echo "    4. ARConv 全部替换（9层）"
    echo ""
    echo "  训练参数:"
    echo "    Epochs: 150"
    echo "    Batch: 40"
    echo "    Workers: 8"
    echo "    Cache: True"
    echo ""
    echo "  预计时间: 约4.8小时"
    echo "  预计成本: 约¥10"
    echo ""
    echo "========================================"
    echo -e "${GREEN}🚀 准备就绪！${NC}"
    echo "========================================"
    echo ""
    echo "下一步："
    echo ""
    echo "1. 启动训练（推荐使用screen）:"
    echo "   screen -S arconv_train"
    echo "   python run_arconv_ablation_experiments.py"
    echo ""
    echo "2. 断开screen（训练继续）:"
    echo "   按 Ctrl+A, 然后按 D"
    echo ""
    echo "3. 重新连接screen:"
    echo "   screen -r arconv_train"
    echo ""
    echo "4. 监控GPU（新终端）:"
    echo "   watch -n 1 nvidia-smi"
    echo ""
    echo "5. 训练完成后分析结果:"
    echo "   python analyze_arconv_ablation.py"
    echo ""
else
    echo -e "${RED}⚠️  部分检查未通过${NC}"
    echo "========================================"
    echo ""
    echo "请解决上述问题后再开始训练"
    echo ""
    exit 1
fi

