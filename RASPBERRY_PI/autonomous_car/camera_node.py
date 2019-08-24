#!/usr/bin/env python
import rospy
import time
import numpy as np
import cv2
import pdb
import sys

class Camera:
    def __init__(self, id):
        # destroy all previous cv instances
        self.device_id = id
        cv2.destroyAllWindows()
        self.device = cv2.VideoCapture(id)
    def take_image():
        return self.device.read()

if __name__ == "__main__":
    pass