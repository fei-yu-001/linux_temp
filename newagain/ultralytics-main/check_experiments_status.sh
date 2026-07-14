#!/bin/bash
# 检查前3个实验的训练状态

echo "检查实验状态..."
echo ""

for exp in arconv_backbone arconv_neck arconv_head; do
    echo "=== $exp ==="
    
    if [ -d "runs/ablation/$exp" ]; then
        echo "✓ 目录存在"
        
        # 检查results.csv
        if [ -f "runs/ablation/$exp/results.csv" ]; then
            lines=$(wc -l < "runs/ablation/$exp/results.csv")
            echo "✓ results.csv存在 ($lines 行)"
            
            # 检查最后几行是否有NaN
            tail -5 "runs/ablation/$exp/results.csv" | grep -i "nan" > /dev/null
            if [ $? -eq 0 ]; then
                echo "⚠️  发现NaN！"
            else
                echo "✓ 没有NaN"
            fi
            
            # 显示训练进度
            echo "训练进度: $(($lines - 1))/150 epochs"
        else
            echo "✗ results.csv不存在"
        fi
        
        # 检查weights
        if [ -f "runs/ablation/$exp/weights/best.pt" ]; then
            echo "✓ best.pt存在"
        else
            echo "✗ best.pt不存在"
        fi
    else
        echo "✗ 目录不存在"
    fi
    
    echo ""
done

echo "=== arconv_full ==="
if [ -d "runs/ablation/arconv_full" ]; then
    echo "✓ 目录存在（已失败，需要重新训练）"
else
    echo "✗ 目录不存在"
fi
