import os
import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as transforms

class GarbageDataset(Dataset):
    def __init__(self, root_dir, transform=None, split='train'):
        self.root_dir = root_dir
        self.transform = transform
        self.split = split
        self.image_dir = os.path.join(root_dir, 'images', split)
        self.label_dir = os.path.join(root_dir, 'labels', split)
        self.image_files = sorted([os.path.join(self.image_dir, f) for f in os.listdir(self.image_dir)])
        self.label_files = sorted([os.path.join(self.label_dir, f) for f in os.listdir(self.label_dir)])

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image = Image.open(self.image_files[idx]).convert('RGB')
        label = torch.load(self.label_files[idx])

        if self.transform:
            image = self.transform(image)

        return image, label
