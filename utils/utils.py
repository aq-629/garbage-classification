import os
import random
import torch
import numpy as np
from PIL import Image

def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

def load_image(image_path):
    image = Image.open(image_path).convert('RGB')
    return image

def save_image(image, output_path):
    image.save(output_path)

def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def collate_fn(batch):
    images, labels = zip(*batch)
    images = torch.stack(images)
    labels = list(labels)
    return images, labels
