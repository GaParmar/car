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

import socket
import cv2
import numpy as np

period = 0.1
samples_per_file = 100



def socket_listener(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 8080))
    while(True):
        data_raw,addr = s.recvfrom(1024)
        data.update(json.loads(data_raw))


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

    manager = Manager()

    data = manager.dict()

    socket_process = Process(target=socket_listener, args=(data,))
    socket_process.start()

    log_buffer = []
    log_file_counter = 0

    STATE = "log"

    while True:
        start_main = time.time()
        # get user data from server


        new_data = dict(data)

        # get image from the camera
        status, img = device.read()
        ts = time.time()
        # write to motor
        m.send_data(new_data)

        #log
        if new_data["log_status"] == "LOGGING":
            log_packet = {
                "throttle":new_data["throttle"],
                "steer":new_data["steer"],
                "image":img,
                "timestamp":ts
            }
            log_buffer.append(log_packet)

        if len(log_buffer)>=samples_per_file:
            # start a new sub process to save to file
            p = Process(target=save_to_file, args=(new_data["log_dir"],log_file_counter, deepcopy(log_buffer)))
            p.start()
            log_buffer = []
            log_file_counter += 1


        while time.time()-start_main < period:
            pass
