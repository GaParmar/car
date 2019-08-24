#!/usr/bin/env python
import rospy
import time
import numpy as np
from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import pdb
import sys

class Camera:
    """
    Initialize the camera object with the given device id
    """
    def __init__(self, id=0):
        # destroy all previous cv instances
        self.device_id = id
        cv2.destroyAllWindows()
        self.device = cv2.VideoCapture(id)
    
    """
    Take an image from the device
    """
    def take_image(self):
        return self.device.read()

    """
    Release the device when the camera is to be close
    """
    def close(self):
        self.device.release()

if __name__ == "__main__":
    args = {
        "node_name"         : "camera_node",
        "topic_name"        : "camera_frames",
        "rate"              : 0.1,
    }
    # Initilize the ros publisher node
    rospy.init_node(args["node_name"])
    pub = rospy.Publisher(args["topic_name"], Image, queue_size=1)
    # make the camera object
    camera = Camera()
    while not rospy.is_shutdown():
        start = time.time()
        # take a new image and publish it
        status,img = camera.take_image()
        image = Image()
        image.data = img.flatten().tolist()
        pub.publish(image)
        # busy wait while frequency requirement is met
        while(time.time()-start < args["rate"]):
            pass
    camera.close()
