import os
import torch
import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import pickle

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

class CarDataset(Dataset):
    def __init__(self, fname):
        self.fname = fname
        f = open(fname, "rb")
        data = pickle.load(f)
        f.close()
        self.images = data["X"]
        self.throttle_steer = data["Y"]
        assert len(self.images)==len(self.throttle_steer)
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img = self.images[idx]
        # split the image into left and right
        img_L = torch.from_numpy(self.images[idx][:,0:320,:])
        img_R = torch.from_numpy(self.images[idx][:,320:,:])
        sample = {
            "image_left":img_L,
            "image_right": img_R,
            "throttle":self.throttle_steer[idx][0],
            "steer": self.throttle_steer[idx][1]
        }
        return sample

def data_keras(fname):
    f = open(fname)
    data = pickle.load(f)
    f.close()
    images = data["X"]
    throttle_steer = data["Y"]
    num = len(images)
    X = []
    Y = []
    for i in range(100):
        img_L = torch.from_numpy(images[i][:,0:320,:])
        img_R = torch.from_numpy(images[i][:,320:,:])
        stack = np.concatenate((img_L, img_R), axis=2)
        X.append(stack)
        Y.append([throttle_steer[0], throttle_steer[1]])
    X = np.array(X)
    Y = np.array(Y)
    return X,Y