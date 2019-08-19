import keras
from train_model.model import make_model
from keras.models import load_model

from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform

import pdb

class Pilot():
    def __init__(self, path):
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            self.M = load_model(path)

pdb.set_trace()
p = Pilot("ckpt-100-0.0836.hdf5")