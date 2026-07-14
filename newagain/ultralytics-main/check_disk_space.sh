#!/bin/bash
# 检查磁盘空间使用情况
# 使用方法: bash check_disk_space.sh

echo "======================================"
echo "磁盘空间检查"
echo "======================================"

# 总体磁盘使用
echo ""
echo "总体磁盘使用:"
df -h | grep -E "Filesystem|/$|/data"

# 项目目录大小
echo ""
echo "项目目录大小:"
if [ -d "domestic_dataset" ]; then
    echo "数据集: $(du -sh domestic_dataset 2>/dev/null | cut -f1)"
fi

if [ -d "runs" ]; then
    echo "训练结果: $(du -sh runs 2>/dev/null | cut -f1)"
fi

if [ -d "logs" ]; then
    echo "日志文件: $(du -sh logs 2>/dev/null | cut -f1)"
fi

# 各模型结果大小
echo ""
echo "各模型结果大小:"
if [ -d "runs/train" ]; then
    for dir in runs/train/*/; do
        if [ -d "$dir" ]; then
            size=$(du -sh "$dir" 2>/dev/null | cut -f1)
            name=$(basename "$dir")
            echo "  $name: $size"
        fi
    done
fi

# 可用空间
echo ""
echo "可用空间:"
df -h . | tail -1 | awk '{print "  剩余: " $4 " / " $2 " (使用率: " $5 ")"}'

# 空间警告
available=$(df . | tail -1 | awk '{print $4}')
if [ $available -lt 5242880 ]; then  # 小于5GB
    echo ""
    echo "⚠️  警告: 可用空间不足5GB，建议清理！"
fi

echo "======================================"
