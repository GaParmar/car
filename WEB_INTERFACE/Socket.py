import socket

ETHERNET_IP="192.168.2.9"
WIFI_IP="192.168.4.19"

class Socket:
    def __init__(self, ip=ETHERNET_IP, port=8080):
        self.car_ip = ip
        self.car_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        val =  '{ "throttle":%f,'%data["thrust"]
        val += '"direction": "forward", '
        val += '"steer":%f, '%data["steer"]
        val += '"log_status": "%s", '%(str(data["log_status"]))
        val += '"manual_status": "%s", '%(str(data["manual_status"]))
        val += '"log_dir": "%s"}'%(str(data["log_dir"]))
        self.sock.sendto(str.encode(val), (self.car_ip,
                                            self.car_port))
