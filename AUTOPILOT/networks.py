import keras
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.models import Sequential
from keras.layers import Activation

def make_mobilenet_model():
    m = MobileNetV2(input_shape=(240, 320, 6), include_top=True,
                weights=None,classes=2, alpha=0.5)
    wrapper = Sequential()
    wrapper.add(m)
    wrapper.add(Activation('sigmoid'))
    return wrapper