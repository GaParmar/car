#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String, Float32
from smbus2 import SMBus

class ArduinoMotor:
    def __init__(self):
        self.state = {
            "throttle"  : -1,
            "steer"     : 0,
            "direction" : "forward"
        }
        self.arduino_i2c_addr = 0x8

if __name__ == "__main__":
    args = {
        "node_name"         : "motor_node",
        "rate"              : 0.1,
    }
    rospy.init_node(args["node_name"])

    m = ArduinoMotor()
    
    # listen to relevant topic from socket server node
    rospy.Subscriber("update_throttle", Float32,
                        lambda data: m.state["throttle"] = data.data)
    rospy.Subscriber("update_direction", String,
                        lambda data: m.state["direction"] = data.data)
    rospy.Subscriber("update_steer_angle", Float32,
                        lambda data: m.state["steer"] = data.data)

    while not rospy.is_shutdown():

