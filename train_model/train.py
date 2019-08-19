import numpy as np
import torch
from torch.utils.data import DataLoader

from dataset import CarDataset, data_keras
from model import make_model

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

import pdb

data_pkl = "/Users/gauravparmar/Desktop/CAR/DATA/dataset_ftable.pkl"

if __name__ == "__main__":
    print("training the model")
    pdb.set_trace()
    X,Y = data_keras(data_pkl)
    model = make_model()
    opt = keras.optimizers.Adam(lr=0.001 , decay=0.0)
    model.compile(optimizer=opt,
                        metrics=['acc'],
                        loss={'angle_out': 'categorical_crossentropy', 
                                'throttle_out': 'categorical_crossentropy'},
                        loss_weights={'angle_out': 0.5,
                                      'throttle_out': 1.0})


    # ds = CarDataset(data_pkl)
    # dl = DataLoader(ds, batch_size=4, shuffle=True, num_workers=4)
    # print("iterating through the dataset")
    # # go through the dataset
    # for i,batch in enumerate(dl):
    #     print("batch number %d"%i)
    #     # shape batch, height, width, channel
    #     # 4 x 240 x 320 x 3
    #     left = batch["image_left"]
    #     right = batch["image_right"]
    #     pdb.set_trace()
        
        