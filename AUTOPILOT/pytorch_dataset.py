import os
import sys
import pdb
import pickle

import numpy as np
import torch
from torch.utils.data import Dataset
from PIL import Image
import json

class AutonomousCarDataset(Dataset):
  """
  args:
    all_files - list of all files to use
    transform_sample - the transformations to apply to the sample
  """
  def __init__(self, all_files, transform_sample=None):
    self.all_files = all_files
    self.transform_sample = transform_sample
    if not self.transform_sample:
        self.transform_sample = lambda x: x
    all_files.sort()

  """
  Get the total number of samples in the dataset
  """
  def __len__(self):
    return len(self.all_files)

  """
  Get the sample at the given index
  """
  def __getitem__(self, idx):
    curr_path = self.all_files[idx]
    with open(curr_path, "rb") as f:
      raw_sample = pickle.load(f)
    sample = { "image"      : Image.fromarray(raw_sample["image"].astype(np.uint8)),
               "throttle"   : raw_sample["throttle"],
               "steer"      : raw_sample["steer"],
               "path"       : curr_path}
    sample = self.transform_sample(sample)
    return sample