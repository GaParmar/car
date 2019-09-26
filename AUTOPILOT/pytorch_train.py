#%%
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
dataset_dirs = ["./prepared_data/ucsd_track_0",
                "./prepared_data/ucsd_track_1",
                "./prepared_data/ucsd_track_2"]
SPLIT_RATIO = 0.8
EPOCHS = 50

if __name__ == "__main__":
 
    if(not os.path.exists("saved_models")):
        os.makedirs("saved_models")

    # set the random seeds
    np.random.seed(SEED)
    torch.backends.cudnn.deterministic = True
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)

    # Make the datasets
    all_file_paths = []
    # get a list of all files in the preprocessed pkl
    for path in dataset_dirs:
        for file in os.listdir(path):
            if ".pkl" in file:
                all_file_paths.append(os.path.join(path, file))
    
    all_file_paths.sort()
    num_train = int(len(all_file_paths)*SPLIT_RATIO)
    train_paths = all_file_paths[0:num_train]
    test_paths = all_file_paths[num_train:]

    train_set = AutonomousCarDataset(all_files=train_paths,
                        transform_sample=transform_sample)
    test_set = AutonomousCarDataset(all_files=test_paths,
                        transform_sample=transform_sample)
    train_loader = DataLoader(train_set, batch_size=20,
                        shuffle=True, num_workers=4)
    test_loader = DataLoader(test_set, batch_size=20,
                        shuffle=True, num_workers=4)

    # define the model
    model =  MobilenetV2Pilot(pretrained_weights=True)

    if torch.cuda.is_available():
        model.to('cuda')

    optim = torch.optim.Adam(model.parameters(), lr=1e-5)
    scheduler = StepLR(optim, step_size=5, gamma=0.5)
    crit = nn.L1Loss()

    train_losses = []
    test_losses = []

    # start training
    for epoch in range(EPOCHS):
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

            if torch.cuda.is_available():
                left = left.to('cuda')
                right = right.to('cuda')
                gt = gt.to('cuda')
            pred = model(left, right)
            loss = crit(pred, gt)
            loss.backward()
            optim.step()
            train_epoch_loss += loss
        train_epoch_loss /= len(train_loader)
        train_losses.append(train_epoch_loss)
        print("epoch %d training loss: %.6f"%(epoch, train_epoch_loss))
        
        torch.cuda.empty_cache()
        scheduler.step()

        # eval on test set
        model.eval()
        with torch.no_grad():
            test_epoch_loss = 0.0
            for i, sample in enumerate(test_loader):
                left = sample["image_left"]
                right = sample["image_right"]
                throttle = sample["throttle"].reshape(-1,1)
                steer = sample["steer"].reshape(-1,1)
                gt = torch.cat((throttle, steer), 1).float()

                if torch.cuda.is_available():
                    left = left.to('cuda')
                    right = right.to('cuda')
                    gt = gt.to('cuda')

                pred = model(left, right)

                loss = crit(pred, gt)
                test_epoch_loss += loss

            test_epoch_loss /= len(test_loader)
            test_losses.append(test_epoch_loss)
            print("epoch %d test loss: %.6f"%(epoch, test_epoch_loss))
            torch.cuda.empty_cache()

            path = os.path.join("saved_models", "EPOCH_{}_TESTLOSS_{}.statedict".format(epoch, test_epoch_loss))

            torch.save(model.state_dict(), path)

#%%

import matplotlib.pyplot as plt

epoch_range = [i + 1 for i in range(EPOCHS)]
plt.plot(epoch_range, train_losses, label = "train_epoch_loss")
plt.plot(epoch_range, test_losses, label = "test_epoch_loss")
plt.ylabel = "loss"
plt.xlabel = "epoch"
plt.show()

#%%
