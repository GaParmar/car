import time
from subprocess import Popen, PIPE 
from multiprocessing.connection import Listener
import socket
import json
import cv2
import pdb
import numpy as np
from arduino_motor import ArduinoMotor


if __name__ == "__main__":

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind(('', 8080))

    cv2.destroyAllWindows()
    device = cv2.VideoCapture(0)

    # start the process listening to incoming socket
    # d_process["socket"] = Popen(['python3', './socket_process.py'])
    # d_listeners["socket"] = Listener(('localhost', 6000), authkey=b"secret")
    # d_conns["socket"] = d_listeners["socket"].accept()
        # data = d_conns["socket"].recv()
        # print(data)

    # test the ncs

    m = ArduinoMotor()
    
    

    net = cv2.dnn.readNet("mobilenetv2.xml", "mobilenetv2.bin")
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
    

    # the main loop
    while True:

        ret, frame = device.read()

        left = frame[:,:320]
        right = frame[:,320:]


        blob = cv2.dnn.blobFromImage(left, 1.0, (320, 240), (104.0, 177.0, 123.0))
        net.setInput(blob, "left")

        blob = cv2.dnn.blobFromImage(right, 1.0, (320, 240), (104.0, 177.0, 123.0))
        net.setInput(blob, "right")

        out = net.forward()

        throttle = out[0][0] * 15 + 90
        steer = out[0][1] * 60 + 60

        socket.bind(('', 8080))
        data_raw,addr = socket.recvfrom(1024)
        data = json.loads(data_raw)
        socket.close()

        if(data["log_status"] != "INFERENCE"):
            data = {
                "throttle":throttle,
                "steer":steer,
            }

        m.send_data(data)

