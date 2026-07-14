"""
快速测试脚本 - 验证环境配置
上传到服务器后先运行这个，确保环境正常
使用方法: python quick_test.py
"""
import sys

def test_environment():
    print("="*60)
    print("YOLO训练环境测试")
    print("="*60)
    
    # 1. 测试Python版本
    print("\n[1/5] Python版本检查...")
    print(f"Python版本: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要 >= 3.8")
        return False
    print("✓ Python版本正常")
    
    # 2. 测试PyTorch
    print("\n[2/5] PyTorch检查...")
    try:
        import torch
        print(f"PyTorch版本: {torch.__version__}")
        print("✓ PyTorch已安装")
    except ImportError:
        print("❌ PyTorch未安装")
        print("安装命令: pip install torch torchvision")
        return False
    
    # 3. 测试CUDA
    print("\n[3/5] CUDA检查...")
    if torch.cuda.is_available():
        print(f"✓ CUDA可用")
        print(f"  CUDA版本: {torch.version.cuda}")
        print(f"  GPU数量: {torch.cuda.device_count()}")
        print(f"  GPU名称: {torch.cuda.get_device_name(0)}")
        
        # 显存信息
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"  GPU显存: {gpu_mem:.1f} GB")
        
        if gpu_mem < 10:
            print("⚠️  警告: 显存可能不足，建议 >= 12GB")
    else:
        print("❌ CUDA不可用！")
        print("请检查:")
        print("  1. 是否选择了GPU服务器")
        print("  2. CUDA驱动是否正确安装")
        return False
    
    # 4. 测试ultralytics
    print("\n[4/5] Ultralytics检查...")
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics已安装")
    except ImportError:
        print("❌ Ultralytics未安装")
        print("安装命令: pip install ultralytics")
        return False
    
    # 5. 测试数据集路径
    print("\n[5/5] 数据集检查...")
    import os
    if os.path.exists('domestic_dataset/data.yaml'):
        print("✓ 数据集配置文件存在")
        
        # 检查数据集目录
        if os.path.exists('domestic_dataset/images/train'):
            print("✓ 训练集目录存在")
        else:
            print("⚠️  警告: 训练集目录不存在")
            
        if os.path.exists('domestic_dataset/images/val'):
            print("✓ 验证集目录存在")
        else:
            print("⚠️  警告: 验证集目录不存在")
    else:
        print("⚠️  警告: 数据集配置文件不存在")
        print("请确保已上传 domestic_dataset 目录")
    
    print("\n" + "="*60)
    print("✓ 环境测试完成！可以开始训练")
    print("="*60)
    print("\n运行训练:")
    print("  单个模型: python train_yolo11.py")
    print("  全部模型: python run_all_experiments.py")
    print("  后台运行: bash start_experiments.sh")
    print("="*60)
    
    return True

if __name__ == '__main__':
    try:
        success = test_environment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        sys.exit(1)
