import os
import sys
import pdb

from dataset import DataGenerator
from transforms import transform_image, transform_target

dataset_root = "./prepared_data/test_verano_room_stand"
SPLIT_RATIO = 0.8



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

    pdb.set_trace()
    train_loader = DataGenerator(train_paths, batch_size=1, size=(240,640,3),
                        shuffle=False, transform_target=transform_target,
                        transform_image=transform_image)
    train_loader[0]

