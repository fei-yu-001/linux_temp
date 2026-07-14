"""
ARConv训练回调
用于在训练过程中更新ARConv的epoch参数
"""

from ultralytics.nn.modules.conv import ARConv


def on_train_epoch_start(trainer):
    """
    在每个epoch开始时更新ARConv的epoch参数
    
    Args:
        trainer: Ultralytics训练器实例
    """
    current_epoch = trainer.epoch
    ARConv.set_epoch(current_epoch)
    
    # 可选：打印当前epoch（仅在第一个epoch和每10个epoch打印一次）
    if current_epoch == 0 or (current_epoch + 1) % 10 == 0:
        print(f"ARConv: 设置epoch为 {current_epoch}")


# 回调字典，可以直接传递给训练器
arconv_callbacks = {
    'on_train_epoch_start': on_train_epoch_start
}


# 使用示例
if __name__ == '__main__':
    from ultralytics import YOLO
    
    # 加载模型
    model = YOLO('ultralytics/cfg/models/11/yolo11n_arconv_full.yaml')
    
    # 训练时添加回调
    results = model.train(
        data='/root/autodl-tmp/domestic_dataset/data.yaml',
        epochs=150,
        batch=16,
        imgsz=640,
        callbacks=arconv_callbacks  # 添加ARConv回调
    )
