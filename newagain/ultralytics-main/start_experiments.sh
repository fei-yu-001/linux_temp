#!/bin/bash
# YOLO模型对比实验 - 后台运行脚本
# 使用方法: bash start_experiments.sh

echo "======================================"
echo "YOLO模型对比实验 - 启动中"
echo "======================================"

# 检查GPU
echo "检查GPU状态..."
nvidia-smi

# 创建日志目录
mkdir -p logs

# 获取当前时间
timestamp=$(date +"%Y%m%d_%H%M%S")

# 后台运行实验
echo ""
echo "开始批量训练，日志保存到: logs/experiment_${timestamp}.log"
echo "可以使用以下命令查看实时日志:"
echo "  tail -f logs/experiment_${timestamp}.log"
echo ""

nohup python run_all_experiments.py > logs/experiment_${timestamp}.log 2>&1 &

# 获取进程ID
pid=$!
echo "训练进程已启动，PID: $pid"
echo "进程ID已保存到: logs/experiment.pid"
echo $pid > logs/experiment.pid

echo ""
echo "======================================"
echo "常用命令:"
echo "  查看日志: tail -f logs/experiment_${timestamp}.log"
echo "  查看进程: ps -p $pid"
echo "  停止训练: kill $pid"
echo "======================================"
