import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('ultralytics/cfg/models/11/yolo11.yaml')
    model.train(
        data='domestic_dataset/data.yaml',
        cache=True,  # 开启缓存，提速15-20%
        imgsz=640,
        epochs=150,
        batch=16,
        close_mosaic=10,
        workers=8,
        device='0',
        optimizer='SGD',
        amp=True,  # 混合精度训练，提速30-50%
        project='runs/train',
        name='yolo11_one',  
    )
