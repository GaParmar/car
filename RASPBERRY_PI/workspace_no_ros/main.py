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
    rnd = np.zeros((1,3,320,240))
    net = cv2.dnn.readNet("mobilenetv2.xml", "mobilenetv2.bin")
    net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)


    # the main loop
    while True:
        start = time.time()

        data_raw,addr = socket.recvfrom(1024)
        data = json.loads(data_raw)

        status, img = device.read()
        
        pdb.set_trace()


        while time.time()-start < 1:
            pass
