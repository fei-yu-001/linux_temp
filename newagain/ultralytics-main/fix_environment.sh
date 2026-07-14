#!/bin/bash
# Fix corrupted Python environment

echo "=== Step 1: Backup current environment ==="
cd ~
mv miniconda3 miniconda3_broken_backup

echo "=== Step 2: Download fresh Miniconda ==="
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

echo "=== Step 3: Install Miniconda ==="
bash miniconda.sh -b -p ~/miniconda3

echo "=== Step 4: Initialize conda ==="
~/miniconda3/bin/conda init bash
source ~/.bashrc

echo "=== Step 5: Create new environment ==="
~/miniconda3/bin/conda create -n yolo python=3.8 -y

echo "=== Step 6: Activate environment ==="
source ~/miniconda3/bin/activate yolo

echo "=== Step 7: Install PyTorch with CUDA ==="
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "=== Step 8: Install Ultralytics and dependencies ==="
pip install ultralytics opencv-python pillow pyyaml -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "=== Step 9: Verify installation ==="
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
python -c "from ultralytics import YOLO; print('Ultralytics imported successfully')"

echo "=== Environment fixed! ==="
echo "To use the new environment, run:"
echo "  source ~/miniconda3/bin/activate yolo"
echo "  cd ~/YOLOv11"
echo "  python train_yolo11_domestic.py"
