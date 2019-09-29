import time
from subprocess import Popen, PIPE 
from multiprocessing.connection import Listener
import socket
import json
import cv2
import pdb
import numpy as np

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
    pdb.set_trace()
    image = cv2.imread("face.png")
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (320, 240)), 1.0, (320, 240), (104.0, 177.0, 123.0))

    net = cv2.dnn.readNet("mobilenetv2.xml", "mobilenetv2.bin")
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
    
    net.setInput(blob, "left")
    net.setInput(blob, "right")
    out = net.forward()

    # the main loop
    while True:
        start = time.time()

        data_raw,addr = socket.recvfrom(1024)
        data = json.loads(data_raw)

        status, img = device.read()
        
        pdb.set_trace()


        while time.time()-start < 1:
            pass
