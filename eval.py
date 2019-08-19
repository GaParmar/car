import numpy as np
import torch
from torch.utils.data import DataLoader

from train_model.dataset import CarDataset, data_keras
from train_model.model import make_model

import pdb

model_path = "./ckpt-100-0.0836.hdf5"
img_path = ""

if __name__ == "__main__":
    pdb.set_trace()
    model = make_model()
