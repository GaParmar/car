import os
import sys
import pdb

import keras

from dataset import DataGenerator
from transforms import transform_image, transform_target
from networks import make_mobilenet_model

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
    train_loader = DataGenerator(train_paths, batch_size=10, size=(240,320,6),
                        shuffle=False, transform_target=transform_target,
                        transform_image=transform_image)
    test_loader = DataGenerator(test_paths, batch_size=10, size=(240,320,6),
                        shuffle=False, transform_target=transform_target,
                        transform_image=transform_image)
    model = make_mobilenet_model()

    opt = keras.optimizers.Adam(lr=0.001 , decay=0.0)
    model.compile(optimizer=opt,
                    metrics=['acc'],
                    loss='mse')

    model.fit_generator(generator=train_loader,
                        validation_data=test_loader,
                        steps_per_epoch = len(train_loader),
                        epochs=5,
                        use_multiprocessing=True,
                        workers=2)
