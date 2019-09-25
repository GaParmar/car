import numpy as np


def transform_target(data):
    throttle = data[0]
    steer = data[1]
    # normalize throttle to range [0,1] from [90, 90+15]
    throttle -= 90
    throttle /= 15.0
    # normalize steer to range [0,1] from [60,120]
    steer -= 60
    steer /= 60.0
    return [throttle, steer]

def transform_image(data):
    # normalize to range [0,1] from [0,255]
    data /= 255.0
    # change shape from [240, 640, 3] to [240, 320, 6]
    left = data[:,0:320,:]
    right = data[:,320:,:]
    data = np.concatenate((left, right), axis=2)
    return data