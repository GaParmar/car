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
        self.i2c_bus = SMBus(1)

    def send_data(self):
        # send the throttle first
        data = [ord('t'), int(self.state["throttle"])]
        self.i2c_bus.write_i2c_block_data(self.arduino_i2c_addr,0,data)
        # senf the steering angle next
        data = [ord('s'), int(self.state["steer"])]
        self.i2c_bus.write_i2c_block_data(self.arduino_i2c_addr,0,data)

if __name__ == "__main__":
    args = {
        "node_name"         : "motor_node",
        "rate"              : 0.1,
    }
    rospy.init_node(args["node_name"])

    m = ArduinoMotor()
    
    # listen to relevant topic from socket server node
    rospy.Subscriber("update_throttle", Float32,
                        lambda data: m.state["throttle"] = int(data.data))
    rospy.Subscriber("update_direction", String,
                        lambda data: m.state["direction"] = data.data)
    rospy.Subscriber("update_steer_angle", Float32,
                        lambda data: m.state["steer"] = int(data.data))

    while not rospy.is_shutdown():
        start = time.time()
        m.send_data()
        # busy wait while frequency requirement is met
        while(time.time()-start < args["rate"]):
            pass
