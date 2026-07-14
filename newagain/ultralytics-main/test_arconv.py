#!/usr/bin/env python3
"""
ARConv模块测试脚本
验证ARConv模块是否正确实现和可用
"""

import torch
import sys

def test_arconv_import():
    """测试ARConv模块导入"""
    print("测试1: 导入ARConv模块...")
    try:
        from ultralytics.nn.modules import ARConv
        print("✓ ARConv模块导入成功")
        return True
    except ImportError as e:
        print(f"✗ ARConv模块导入失败: {e}")
        return False

def test_arconv_creation():
    """测试ARConv模块创建"""
    print("\n测试2: 创建ARConv实例...")
    try:
        from ultralytics.nn.modules import ARConv
        
        # 创建ARConv实例
        arconv = ARConv(c1=64, c2=128, k=3, s=1)
        print(f"✓ ARConv实例创建成功")
        print(f"  输入通道: 64, 输出通道: 128, 卷积核: 3x3")
        return True, arconv
    except Exception as e:
        print(f"✗ ARConv实例创建失败: {e}")
        return False, None

def test_arconv_forward():
    """测试ARConv前向传播"""
    print("\n测试3: 测试ARConv前向传播...")
    try:
        from ultralytics.nn.modules import ARConv
        
        # 创建ARConv实例
        arconv = ARConv(c1=64, c2=128, k=3, s=1)
        
        # 创建测试输入
        x = torch.randn(2, 64, 32, 32)  # (batch, channels, height, width)
        print(f"  输入形状: {x.shape}")
        
        # 前向传播
        output = arconv(x)
        print(f"  输出形状: {output.shape}")
        
        # 验证输出形状
        expected_shape = (2, 128, 32, 32)
        if output.shape == expected_shape:
            print(f"✓ 前向传播成功，输出形状正确")
            return True
        else:
            print(f"✗ 输出形状错误，期望 {expected_shape}，得到 {output.shape}")
            return False
            
    except Exception as e:
        print(f"✗ 前向传播失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_arconv_parameters():
    """测试ARConv参数"""
    print("\n测试4: 检查ARConv参数...")
    try:
        from ultralytics.nn.modules import ARConv
        
        arconv = ARConv(c1=64, c2=128, k=3, s=1)
        
        # 统计参数数量
        total_params = sum(p.numel() for p in arconv.parameters())
        trainable_params = sum(p.numel() for p in arconv.parameters() if p.requires_grad)
        
        print(f"  总参数数: {total_params:,}")
        print(f"  可训练参数数: {trainable_params:,}")
        print(f"✓ 参数检查完成")
        return True
        
    except Exception as e:
        print(f"✗ 参数检查失败: {e}")
        return False

def test_model_loading():
    """测试加载使用ARConv的模型配置"""
    print("\n测试5: 加载ARConv模型配置...")
    try:
        from ultralytics import YOLO
        
        # 尝试加载ARConv配置
        configs = [
            'ultralytics/cfg/models/11/yolo11n_arconv_backbone.yaml',
            'ultralytics/cfg/models/11/yolo11n_arconv_head.yaml',
            'ultralytics/cfg/models/11/yolo11n_arconv_full.yaml',
        ]
        
        for config in configs:
            print(f"  加载配置: {config}")
            model = YOLO(config)
            print(f"  ✓ 配置加载成功")
        
        print(f"✓ 所有模型配置加载成功")
        return True
        
    except Exception as e:
        print(f"✗ 模型配置加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("="*70)
    print("ARConv模块测试")
    print("="*70)
    
    results = []
    
    # 运行所有测试
    results.append(("导入测试", test_arconv_import()))
    
    success, arconv = test_arconv_creation()
    results.append(("创建测试", success))
    
    if success:
        results.append(("前向传播测试", test_arconv_forward()))
        results.append(("参数测试", test_arconv_parameters()))
    
    results.append(("模型加载测试", test_model_loading()))
    
    # 打印测试总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {test_name}")
    
    print("-"*70)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n✓ 所有测试通过！ARConv模块已正确实现。")
        print("可以开始运行消融实验了。")
        return 0
    else:
        print(f"\n✗ 有 {total - passed} 个测试失败，请检查实现。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
