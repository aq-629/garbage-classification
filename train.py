import torch
from torch.utils.data import DataLoader
from ultralytics import YOLO
from utils.dataset import GarbageDataset
from utils.transforms import get_transforms
from utils.utils import collate_fn

def train():
    # 加载数据集
    train_dataset = GarbageDataset(root_dir='data', transform=get_transforms(), split='train')
    val_dataset = GarbageDataset(root_dir='data', transform=get_transforms(), split='val')

    # 创建数据加载器
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, collate_fn=collate_fn)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False, collate_fn=collate_fn)

    # 加载预训练模型
    model = YOLO('models/yolov8n.pt')

    # 训练模型
    model.train(data='config/yolov8n.yaml', epochs=50, batch=32, imgsz=640, device=0, workers=8, project='garbage-classification', name='train')

if __name__ == '__main__':
    train()
