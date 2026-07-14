#!/bin/bash
# 清理不必要的文件以节省空间
# 使用方法: bash cleanup_space.sh

echo "======================================"
echo "空间清理工具"
echo "======================================"

# 显示当前空间
echo ""
echo "清理前空间:"
df -h . | tail -1 | awk '{print "  可用: " $4 " / " $2}'

# 清理选项
echo ""
echo "请选择清理选项:"
echo "1. 清理Python缓存 (__pycache__, *.pyc)"
echo "2. 清理pip缓存"
echo "3. 清理训练中间文件（保留best.pt和last.pt）"
echo "4. 清理所有训练结果（危险！）"
echo "5. 全部清理（1+2+3）"
echo "0. 取消"
echo ""
read -p "请输入选项 (0-5): " choice

case $choice in
    1)
        echo "清理Python缓存..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        find . -type f -name "*.pyc" -delete 2>/dev/null
        echo "✓ Python缓存已清理"
        ;;
    2)
        echo "清理pip缓存..."
        pip cache purge
        echo "✓ pip缓存已清理"
        ;;
    3)
        echo "清理训练中间文件..."
        if [ -d "runs/train" ]; then
            for dir in runs/train/*/; do
                if [ -d "$dir" ]; then
                    # 保留weights目录和results.csv
                    find "$dir" -type f ! -path "*/weights/*" ! -name "results.csv" -delete 2>/dev/null
                    echo "  清理: $(basename $dir)"
                fi
            done
        fi
        echo "✓ 训练中间文件已清理"
        ;;
    4)
        read -p "确认删除所有训练结果？(yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            rm -rf runs/train/*
            echo "✓ 所有训练结果已删除"
        else
            echo "已取消"
        fi
        ;;
    5)
        echo "执行全部清理..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        find . -type f -name "*.pyc" -delete 2>/dev/null
        pip cache purge
        if [ -d "runs/train" ]; then
            for dir in runs/train/*/; do
                if [ -d "$dir" ]; then
                    find "$dir" -type f ! -path "*/weights/*" ! -name "results.csv" -delete 2>/dev/null
                fi
            done
        fi
        echo "✓ 全部清理完成"
        ;;
    0)
        echo "已取消"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

# 显示清理后空间
echo ""
echo "清理后空间:"
df -h . | tail -1 | awk '{print "  可用: " $4 " / " $2}'

echo "======================================"
