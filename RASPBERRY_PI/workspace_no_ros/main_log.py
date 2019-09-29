import os
import sys
import time
import pickle
import pdb
import json
from copy import deepcopy

from multiprocessing.connection import Listener
from multiprocessing import Process

import socket
import cv2
import numpy as np

period = 0.1
samples_per_file = 100

class ArduinoMotor:
    def __init__(self, addr=0x8):
        self.arduino_i2c_addr = addr
        self.i2c_bus = SMBus(1)
    def send_data(self, data):
        # send the throttle first
        data = [ord('t'), int(data["throttle"])]
        self.i2c_bus.write_i2c_block_data(self.arduino_i2c_addr,0,data)
        # senf the steering angle next
        data = [ord('s'), int(data["steer"])]
        self.i2c_bus.write_i2c_block_data(self.arduino_i2c_addr,0,data)

def save_to_file(dname, counter, buff):
    if not os.path.exists(dname):
        os.makedirs(dname)
    filename = os.path.join(dname, "log_%d.pkl"%counter)
    with open(fname, "wb") as f:
        pickle.dump(buff, f)

if __name__ == "__main__":
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind(('', 8080))

    cv2.destroyAllWindows()
    device = cv2.VideoCapture(0)

    m = ArduinoMotor()

    log_buffer = []
    log_file_counter = 0

    STATE = "log"

    while True:
        start_main = time.time()
        # get user data from server
        data_raw,addr = socket.recvfrom(1024)
        data = json.loads(data_raw)
        # get image from the camera
        status, img = device.read()
        ts = time.time()
        # write to motor
        m.send_data(data)

        #log
        if data["log_status"] == "LOGGING":
            log_packet = {
                "throttle":data["throttle"],
                "steer":data["steer"],
                "image":img,
                "timestamp":ts
            }
            log_buffer.append(log_packet)

        if len(log_buffer)>=samples_per_file:
            # start a new sub process to save to file
            p = Process(target=save_to_file, args=(data["log_dir"],log_file_counter, deepcopy(log_buffer)))
            p.start()
            log_buffer = []
            log_file_counter += 1


        while time.time()-start < period:
            pass
