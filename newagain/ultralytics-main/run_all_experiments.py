"""
批量运行所有模型对比实验
使用方法：python run_all_experiments.py
"""
import subprocess
import time
from datetime import datetime

# 定义所有实验
experiments = [
    ('YOLOv8n', 'train_yolov8.py'),
    ('YOLO11n', 'train_yolo11.py'),
    ('YOLO12n', 'train_yolo12.py'),
    ('YOLOv9c', 'train_yolov9.py'),
    ('YOLOv10n', 'train_yolov10.py'),
]

def run_experiment(name, script):
    """运行单个实验"""
    print(f"\n{'='*60}")
    print(f"开始训练: {name}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    try:
        # 运行训练脚本
        result = subprocess.run(['python', script], check=True)
        
        elapsed_time = time.time() - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        
        print(f"\n✓ {name} 训练完成！")
        print(f"耗时: {hours}小时 {minutes}分钟")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {name} 训练失败: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n用户中断了 {name} 的训练")
        return False

if __name__ == '__main__':
    print("="*60)
    print("YOLO模型对比实验 - 批量训练")
    print("="*60)
    print(f"共 {len(experiments)} 个模型待训练")
    print("数据集: domestic_dataset (31类昆虫)")
    print("训练参数: epochs=200, batch=16, imgsz=640")
    print("="*60)
    
    results = {}
    total_start = time.time()
    
    for name, script in experiments:
        success = run_experiment(name, script)
        results[name] = 'Success' if success else 'Failed'
        
        # 每个模型训练完后暂停一下
        if success:
            print("\n等待5秒后开始下一个模型...")
            time.sleep(5)
    
    # 打印总结
    total_time = time.time() - total_start
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    
    print("\n" + "="*60)
    print("所有实验完成！")
    print("="*60)
    print(f"总耗时: {hours}小时 {minutes}分钟\n")
    
    print("实验结果:")
    for name, status in results.items():
        symbol = "✓" if status == "Success" else "✗"
        print(f"  {symbol} {name}: {status}")
    
    print("\n结果保存在: runs/train/")
    print("="*60)
