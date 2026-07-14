#!/bin/bash
# 打包ARConv文件用于上传到服务器

echo "开始打包ARConv文件..."

# 创建临时目录
mkdir -p arconv_package

# 复制核心文件
echo "复制核心文件..."
cp ultralytics/nn/modules/conv.py arconv_package/
cp ultralytics/nn/modules/__init__.py arconv_package/
cp ultralytics/cfg/models/11/yolo11n_arconv_minimal.yaml arconv_package/
cp train_ablation_minimal.py arconv_package/

# 复制可选文件
echo "复制可选文件..."
cp test_arconv.py arconv_package/ 2>/dev/null || true
cp IMPORTANT_UPDATE.md arconv_package/ 2>/dev/null || true
cp ARCONV_AUTHOR_CLARIFICATION.md arconv_package/ 2>/dev/null || true
cp CSDN_TUTORIAL_REFERENCE.md arconv_package/ 2>/dev/null || true

# 打包
echo "打包中..."
tar -czf arconv-minimal.tar.gz arconv_package/

# 清理
rm -rf arconv_package/

echo "打包完成！"
echo "文件：arconv-minimal.tar.gz"
echo ""
echo "上传到服务器后，解压命令："
echo "tar -xzf arconv-minimal.tar.gz"
