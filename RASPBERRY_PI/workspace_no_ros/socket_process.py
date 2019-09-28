import socket
import time
from multiprocessing.connection import Client

period = 0.05
port = 8080
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(('', port))
conn = Client(('localhost', 6000), authkey='secret')

while True:
    start = time.time()
    try:
        # get data from socket server
        data_raw,addr = socket.recvfrom(1024)
        data = json.loads(data_raw)
        # pass it along to the localhost
        conn.send(data)
        while time.time()-start < period:
            pass
    except:
        pass
