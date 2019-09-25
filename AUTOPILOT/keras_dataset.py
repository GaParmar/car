import os
import torch
import pickle
import random
import pdb

import numpy as np
import keras

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")



class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    """
    all_files - list of files to make the dataset from
    batch_size - number of samples in a single batch
    size - (H,W,C) tuple
    shuffle - whether to shuffle the order of samples
    transform_image - function to apply to the image
    transform_target - preprocessing for target pair
    """
    def __init__(self, all_files, batch_size=10, size=(240,640,3),
                    shuffle=True, transform_image=None, transform_target=None):
        self.all_files = all_files
        self.size = size
        self.h = size[0]
        self.w = size[1]
        self.c = size[2]
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.indices = np.arange(len(self.all_files))
        self.transform_image = transform_image
        self.transform_target = transform_target
        if not self.transform_image:
            self.transform_image = lambda x:x
        if not self.transform_target:
            self.transform_target = lambda x:x
        if self.shuffle:
            self.all_files = random.shuffle(self.all_files)

    def __len__(self):
        # number of batches per epoch
        return int(np.floor(len(self.all_files) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indices of the batch
        indices= self.indices[index*self.batch_size:(index+1)*self.batch_size]
        # list of paths for the current batch
        batch_paths_list = [self.all_files[k] for k in indices]
        # Generate data
        X, y = self.__data_generation(batch_paths_list)
        return X, y


    def __data_generation(self, batch_paths_list):
        'Generates data containing batch_size samples' 
        # X : (n_samples, H, W, C)
        # Initialization
        X = np.empty((self.batch_size, self.h, self.w, self.c), dtype=float)
        y = np.empty((self.batch_size, 2), dtype=float)

        # Load data from file
        for i, ID in enumerate(batch_paths_list):
            with open(ID, "rb") as f:
                sample = pickle.load(f)
            X[i,] = self.transform_image(sample["image"].astype(np.float32))
            y[i] = self.transform_target([sample["throttle"], sample["steer"]])

        return X, y