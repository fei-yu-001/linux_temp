import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    # YOLOv9c - v9系列推荐版本
    model = YOLO('ultralytics/cfg/models/v9/yolov9c.yaml')
    model.train(
        data='domestic_dataset/data.yaml',
        cache='ram',  # 使用内存缓存，提速15-20%
        imgsz=640,
        epochs=150,
        batch=16,
        close_mosaic=10,
        workers=8,
        device='0',
        optimizer='SGD',
        amp=True,  # 混合精度训练，提速30-50%
        project='runs/train',
        name='yolov9c_domestic',
        val_period=5,  # 每5轮验证一次，节省10-15%时间
        save_period=10,  # 每10轮保存一次，减少IO
    )
