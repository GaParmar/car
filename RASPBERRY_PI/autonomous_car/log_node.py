#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float32
from smbus2 import SMBus
import time
import pdb
import pickle
import os
from copy import deepcopy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import threading


def save_to_file(buff, path):
    with open(path, "wb") as f:
        pickle.dump(buff, f)

class Logger:
    def __init__(self):
        self.buffer = []
        self.current_data = {
            "throttle"  :   -1,
            "steer"     :   -1,
            "timestamp" :   -1,
            "image"     :   None,
        }
        self.log_dir = "/home/pi/temp"
        self.log_status = "STANDBY"
        self.bridge = CvBridge()
        self.file_counter = 0
    def update_throttle(self, data):
        self.current_data["throttle"] = int(data.data)
    def update_steer(self, data):
        self.current_data["steer"] = int(data.data)
    def update_log_dir(self, data):
        self.log_dir = data.data
    def update_log_status(self, data):
        # if going from "STANDBY" to "LOGGING"
        if self.log_status=="STANDBY" and data.data=="LOGGING":
            # make the logging dir if it does not exist
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            self.buffer = []
        # going from "LOGGING" to "STANDBY"
        elif self.log_status=="LOGGING" and data.data=="STANDBY":
            pass 
        self.log_status = data.data
    def update_image(self, data):
        self.current_data["image"] = self.bridge.imgmsg_to_cv2(data, "bgr8")

if(__name__ == "__main__"):
    args = {
        "node_name"         : "log_node",
        "rate"              : 0.05,
        "samples_per_file"  : 100,
    }
    # initialize the rosnode
    rospy.init_node(args["node_name"])
    log = Logger()
    # subscribe to the relevant topics
    rospy.Subscriber("update_throttle", Float32, log.update_throttle)
    rospy.Subscriber("update_steer_angle", Float32, log.update_steer)
    rospy.Subscriber("update_log_status", String, log.update_log_status)
    rospy.Subscriber("update_log_dir", String, log.update_log_dir)
    rospy.Subscriber("camera_frames", Image, log.update_image)
    while not rospy.is_shutdown():
        start = time.time()

        if log.log_status == "LOGGING":
            # add the data object to buffer
            log.current_data["timestamp"] = time.time()
            log.buffer.append(deepcopy(log.current_data))
            if len(log.buffer) > args["samples_per_file"]:
                file_name = os.path.join(log.log_dir,
                                        "log%d.pkl"%log.file_counter)
                # start a new thread to save to file
                t = threading.Thread(target=save_to_file,
                                        args=(log.buffer,file_name))
                t.start()
                # with open(file_name, "wb") as f:
                #     pickle.dump(log.buffer, f)
                log.file_counter += 1
                log.buffer = []

        # busy wait while frequency requirement is met
        while(time.time()-start < args["rate"]):
            pass
