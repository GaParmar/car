#!/usr/bin/env python
import socket
import rospy
from std_msgs.msg import String, Float32
import json
import time

class SocketServer:
    """
    Initialize the socket server that listens to the given port
    and updates at the given rate
    """
    def __init__(self, port, rate):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', port))
        self.state = {
            "throttle"      : 0.0,
            "direction"     : "forward",
            "steer"         : 0.0,
            "log_status"    : "STANDBY",
            "log_dir"       : "~/LOG/default"
        }
        self.port = port
        self.rate = rate
        # make the publishers
        self.pub_throttle = rospy.Publisher("update_throttle",
                                Float32, queue_size=1)
        self.pub_dir = rospy.Publisher("update_direction",
                                String, queue_size=1)
        self.pub_steer = rospy.Publisher("update_steer_angle",
                                Float32, queue_size=1)
        self.pub_log_status = rospy.Publisher("update_log_status",
                                String, queue_size=1)
        self.pub_log_dir = rospy.Publisher("update_log_dir",
                                String, queue_size=1)

    """
    Publishes the contents of the current state to the relative topics
    """
    def publish_topics(self):
        self.pub_throttle.publish(self.state["throttle"])
        self.pub_steer.publish(self.state["steer"])
        self.pub_log_status.publish(self.state["log_status"])
        self.pub_dir.publish(self.state["log_dir"])

    """
    keep listening to the port and publish messages
    """
    def listen(self):
        while not rospy.is_shutdown():
            start = time.time()
            # load the json data received from server
            data_raw,addr = self.socket.recvfrom(1024)
            data = json.loads(data_raw)
            self.state["throttle"] = data["throttle"]
            self.state["direction"] = data["direction"]
            self.state["steer"] = data["steer"]
            self.state["log_status"] = data["log_status"]
            self.state["log_dir"] = data["log_dir"]
            self.publish_topics()
            # busy wait while frequency requirement is met
            while time.time()-start < self.rate:
                pass


if __name__ == "__main__":
    args = {
        "node_name"         : "socket_node",
        "rate"              : 0.01,
        "port"              : 8080
    }
    # initialize the socket server node
    rospy.init_node(args["node_name"])
    socket = SocketServer(args["port"], args["rate"])
    socket.listen()
