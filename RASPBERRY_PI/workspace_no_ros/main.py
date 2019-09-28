import time
from subprocess import Popen, PIPE 
from multiprocessing.connection import Listener

if __name__ == "__main__":
    d_listeners = {}
    d_conns = {}

    # start the process listening to incoming socket
    process = Popen(['python3', './socket_process.py'])
    d_listeners["socket"] = Listener(('localhost', 6000), authkey=b"secret")
    d_conns["socket"] = d_listeners["socket"].accept()

    # the main loop
    while True:
        start = time.time()
        data = d_conns["socket"].recv()
        print(data)
        while time.time()-start < 1:
            pass