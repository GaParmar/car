import time
import socket
import json
import cv2
import pdb
import numpy as np
from arduino_motor import ArduinoMotor
from multiprocessing import Process, Manager
from ps4_interface import PS4Interface


THROTTLE_ALLOWANCE = 20
STEER_ALLOWANCE = 20



def convert_controls(ps4_data, mode):
    if(time.time() - ps4_data["timestamp"] > .5):
        print("disconnected from timestamp")
        return 90, 90, "MANUAL"

    throttle = int((ps4_data["ly"] - 128) * THROTTLE_ALLOWANCE / 128 + 90)
    steer = int((ps4_data["rx"] - 128) * STEER_ALLOWANCE / 128 + 90)

    if(ps4_data["cross"] == 1):
        mode = "INFERENCE"
    if(ps4_data["triangle"] == 1):
        mode = "MANUAL"

    return throttle, steer, mode


if __name__ == "__main__":

    device = cv2.VideoCapture(0)

    m = ArduinoMotor()

    ps4 = PS4Interface()

    net = cv2.dnn.readNet("mobilenetv2.xml", "mobilenetv2.bin")
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
    
    mode = "MANUAL"

    # the main loop
    while True:

        throttle, steer, mode = convert_controls(ps4.data, mode)

        if(mode == "INFERENCE"):
            ret, frame = device.read()

            left = frame[:,:320]
            right = frame[:,320:]


            blob = cv2.dnn.blobFromImage(left, 1.0, (320, 240), (104.0, 177.0, 123.0))
            net.setInput(blob, "left")

            blob = cv2.dnn.blobFromImage(right, 1.0, (320, 240), (104.0, 177.0, 123.0))
            net.setInput(blob, "right")

            out = net.forward()

            throttle = min(out[0][0], 90 + THROTTLE_ALLOWANCE)
            steer = out[0][1]
        else:
            time.sleep(.05)
        
        
        m.send_data({"throttle":throttle, "steer":steer})
