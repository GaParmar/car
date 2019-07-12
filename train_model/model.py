from tensorflow.python.keras.layers import Input
from tensorflow import ConfigProto, Session
from tensorflow.python import keras
from tensorflow.python.keras.layers import Input, Dense
from tensorflow.python.keras.models import Model, Sequential
from tensorflow.python.keras.layers import Convolution2D, MaxPooling2D, Reshape, BatchNormalization
from tensorflow.python.keras.layers import Activation, Dropout, Flatten, Cropping2D, Lambda
from tensorflow.python.keras.layers.merge import concatenate
from tensorflow.python.keras.layers import LSTM

def make_model():
    left_image_in = Input(shape=(240, 320, 3),name='img_left')
    right_image_in = Input(shape=(240, 320, 3),name='img_right')
    # concat into a 6 channel input volume
    x = Concatenate([left_image_in, right_image_in], axis=2)
    # FCN layers
    x = Convolution2D(24, (5, 5), strides=(2, 2), activation='relu')(x)
    x = Convolution2D(32, (5, 5), strides=(2, 2), activation='relu')(x)
    x = Convolution2D(64, (5, 5), strides=(2, 2), activation='relu')(x)
    x = Convolution2D(64, (3, 3), strides=(2, 2), activation='relu')(x)
    x = Convolution2D(64, (3, 3), strides=(1, 1), activation='relu')(x)
    # Dense layers
    x = Flatten(name='flattened')(x)
    x = Dense(100, activation='relu')(x)
    x = Dropout(.1)(x)
    x = Dense(50, activation='relu')(x)
    x = Dropout(.1)(x)
    # Steering angle
    angle = Dense(15, activation='softmax', name='angle_cat_out')(x)
    angle_out = Dense(1, activation='sigmoid', name='angle_out')(angle)
    # throttle output
    throttle_out = Dense(1, activation='relu', name='throttle_out')(x)
    model = Model(inputs=[left_image_in, right_image_in],
                  outputs=[angle_out, throttle_out])
    # model.compile(optimizer='adam',
    #               loss={'angle_out': 'mean_squared_error',
    #                     'throttle_out': 'mean_absolute_error'},
    #               loss_weights={'angle_out': 0.9, 'throttle_out': .01})
    return model