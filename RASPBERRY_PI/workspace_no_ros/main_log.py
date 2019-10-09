import os
import sys
import time
import pickle
import pdb
import json
from copy import deepcopy

from arduino_motor import ArduinoMotor

from multiprocessing.connection import Listener
from multiprocessing import Process, Manager

import cv2
import numpy as np

period = 0.1
samples_per_file = 100


THROTTLE_ALLOWANCE = 20


def convert_controls(ps4_data, mode, log_dir):
    throttle = int((ps4_data["ly"] - 128) * THROTTLE_ALLOWANCE / 128 + 90)
    steer = int(ps4_data["rx"] * 180 / 255)

    if(ps4_data["cross"] == 1):
        if(mode == "NOTLOGGING"):
            log_dir = json.load("config.json")["log_path"]
        mode = "LOGGING"
    if(ps4_data["square"] == 1):
        mode = "NOTLOGGING"

    return throttle, steer, mode, log_dir



def save_to_file(dname, counter, buff):
    if not os.path.exists(dname):
        os.makedirs(dname)
    filename = os.path.join(dname, "log_%d.pkl"%counter)
    with open(fname, "wb") as f:
        pickle.dump(buff, f)

if __name__ == "__main__":
    
    
    device = cv2.VideoCapture(0)

    m = ArduinoMotor()

    ps4 = PS4Interface()

    log_buffer = []
    log_file_counter = 0

    STATE = "NOTLOGGING"

    log_dir = "dab"

    while True:
        start_main = time.time()

        throttle, steer, mode, log_dir = convert_controls(ps4.data, mode, log_dir)

        # get image from the camera
        status, img = device.read()
        ts = time.time()
        # write to motor


        data = {
            "throttle":"throttle",
            "steer":"steer",
            "image":img,
            "timestamp":ts
        }

        m.send_data(data)

        #log
        if STATE == "LOGGING":
            log_buffer.append(data)

        if len(log_buffer)>=samples_per_file:
            # start a new sub process to save to file
            p = Process(target=save_to_file, args=(log_dir, log_file_counter, deepcopy(log_buffer)))
            p.start()
            log_buffer = []
            log_file_counter += 1


        while time.time()-start_main < period:
            pass
