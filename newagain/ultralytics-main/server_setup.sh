#!/bin/bash
# RTX 3080 Ti 服务器环境配置脚本
# 使用方法: bash server_setup.sh

echo "======================================"
echo "YOLO训练环境配置 - 开始"
echo "======================================"

# 1. 检查GPU
echo ""
echo "[1/6] 检查GPU状态..."
nvidia-smi
if [ $? -ne 0 ]; then
    echo "❌ 错误: 未检测到GPU！请检查服务器配置"
    exit 1
fi
echo "✓ GPU检测成功"

# 2. 更新系统
echo ""
echo "[2/6] 更新系统包..."
sudo apt-get update -y

# 3. 安装Python依赖
echo ""
echo "[3/6] 检查Python环境..."
python3 --version
pip3 --version

# 4. 安装ultralytics和依赖
echo ""
echo "[4/6] 安装ultralytics..."
pip3 install ultralytics pandas -i https://pypi.tuna.tsinghua.edu.cn/simple
# 使用清华镜像源加速

# 5. 验证PyTorch和CUDA
echo ""
echo "[5/6] 验证PyTorch和CUDA..."
python3 << EOF
import torch
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"GPU数量: {torch.cuda.device_count()}")
    print(f"GPU名称: {torch.cuda.get_device_name(0)}")
else:
    print("❌ CUDA不可用！")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ PyTorch/CUDA验证失败"
    exit 1
fi
echo "✓ PyTorch和CUDA验证成功"

# 6. 创建工作目录
echo ""
echo "[6/6] 创建工作目录..."
mkdir -p ~/yolo_experiments
mkdir -p ~/yolo_experiments/logs
mkdir -p ~/yolo_experiments/data

echo ""
echo "======================================"
echo "✓ 环境配置完成！"
echo "======================================"
echo ""
echo "下一步:"
echo "1. 上传项目: scp -r ultralytics-main user@server:~/yolo_experiments/"
echo "2. 上传数据集: scp -r domestic_dataset user@server:~/yolo_experiments/ultralytics-main/"
echo "3. 开始训练: cd ~/yolo_experiments/ultralytics-main && python run_all_experiments.py"
echo ""
