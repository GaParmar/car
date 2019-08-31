#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String, Float32
from smbus2 import SMBus

class ArduinoMotor:
    def __init__(self, addr):
        self.state = {
            "throttle"  : 100,
            "steer"     : 90,
            "direction" : "forward"
        }
        self.arduino_i2c_addr = addr
        self.i2c_bus = SMBus(1)

    def send_data(self):
        print(self.state)
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
        "arduino_i2c_addr"  : 0x8
    }
    rospy.init_node(args["node_name"])

    m = ArduinoMotor(args["arduino_i2c_addr"])

    def update_throttle(data):
        m.state["throttle"] = int(data.data)
    def update_direction(data):
        m.state["direction"] = data.data
    def update_steer_angle(data):
        m.state["steer"] = int(data.data)
    
    # listen to relevant topic from socket server node
    rospy.Subscriber("update_throttle", Float32, update_throttle)
    rospy.Subscriber("update_direction", String, update_direction)
    rospy.Subscriber("update_steer_angle", Float32, update_steer_angle)

    while not rospy.is_shutdown():
        start = time.time()
        try:
            m.send_data()
        except:
            print("could not send data")
        # busy wait while frequency requirement is met
        while(time.time()-start < args["rate"]):
            pass
