import sys
import os
import pdb

from PIL import Image
import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

from pytorch_dataset import AutonomousCarDataset

dataset_root = "./prepared_data/test_verano_room_stand"
SPLIT_RATIO = 0.8

def transform_sample(sample):
    image_transform = transforms.Compose([
                            transforms.Resize((320,240)),
                            transforms.ToTensor(),
                            transforms.Normalize(mean=(0,0,0), std=(1,1,1))
                        ])
    # crop and apply transform
    sample["image_left"] = image_transform(sample["image"].crop((0,0,320,240)))
    sample["image_right"] = image_transform(sample["image"].crop((320,0,640,240)))
    # throttle from [90, 105] to [0,1]
    sample["throttle"] -= 90.0
    sample["throttle"] /= 15.0
    # steer from [60,120] to [0,1]
    sample["steer"] -= 60.0
    sample["steer"] /= 60.0
    del sample["image"]
    return sample

if __name__ == "__main__":
    all_file_paths = []
    # get a list of all files in the preprocessed pkl
    for file in os.listdir(dataset_root):
        if ".pkl" in file:
            all_file_paths.append(os.path.join(dataset_root, file))
    all_file_paths.sort()
    num_train = int(len(all_file_paths)*SPLIT_RATIO)
    train_paths = all_file_paths[0:num_train]
    test_paths = all_file_paths[num_train:]

    train_set = AutonomousCarDataset(all_files=train_paths,
                        transform_sample=transform_sample)
    train_loader = DataLoader(train_set, batch_size=10,
                        shuffle=True, num_workers=4)
    
    for i, sample in enumerate(train_loader):
        left = sample["image_left"]
        right = sample["image_right"]
        throttle, steer = sample["throttle"], sample["steer"]
        pdb.set_trace()
        break