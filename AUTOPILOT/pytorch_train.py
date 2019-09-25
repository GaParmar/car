import sys
import os
import pdb

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import StepLR

from networks.pytorch_networks import MobilenetV2Pilot
from pytorch_dataset import AutonomousCarDataset
from pytorch_transforms import transform_sample

SEED = 101
ROOT = "./prepared_data/test_verano_room_stand"
SPLIT_RATIO = 0.1
EPOCHS = 2

if __name__ == "__main__":
    # set the random seeds
    np.random.seed(SEED)
    torch.backends.cudnn.deterministic = True
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)

    # Make the datasets
    all_file_paths = []
    # get a list of all files in the preprocessed pkl
    for file in os.listdir(ROOT):
        if ".pkl" in file:
            all_file_paths.append(os.path.join(ROOT, file))
    all_file_paths.sort()
    num_train = int(len(all_file_paths)*SPLIT_RATIO)
    train_paths = all_file_paths[0:num_train]
    test_paths = all_file_paths[num_train:]

    train_set = AutonomousCarDataset(all_files=train_paths,
                        transform_sample=transform_sample)
    test_set = AutonomousCarDataset(all_files=test_paths,
                        transform_sample=transform_sample)
    train_loader = DataLoader(train_set, batch_size=10,
                        shuffle=True, num_workers=4)
    test_loader = DataLoader(test_set, batch_size=10,
                        shuffle=True, num_workers=4)

    # define the model
    model =  MobilenetV2Pilot(pretrained_weights=True)

    optim = torch.optim.Adam(model.parameters(), lr=1e-5)
    scheduler = StepLR(optim, step_size=5, gamma=0.5)
    crit = nn.L1Loss()

    train_losses = []

    # start training
    for epoch in range(EPOCHS):
        scheduler.step()
        model.train()
        train_epoch_loss = 0.0
        # iterate through training set
        for i, sample in enumerate(train_loader):
            optim.zero_grad()
            left = sample["image_left"]
            right = sample["image_right"]
            throttle = sample["throttle"].reshape(-1,1)
            steer = sample["steer"].reshape(-1,1)
            gt = torch.cat((throttle, steer), 1).float()
            pred = model(left, right)
            loss = crit(pred, gt)
            loss.backward()
            optim.step()
            train_epoch_loss += loss
        train_epoch_loss /= len(train_loader)
        train_losses.append(train_epoch_loss)
        print("epoch %d training loss: %.6f"%(epoch, train_epoch_loss))





