from smbus2 import SMBus

class ArduinoMotor:
    def __init__(self, addr=0x8):
        self.arduino_i2c_addr = addr
        self.i2c_bus = SMBus(1)
    def send_data(self, data):
        # send the throttle first
        data = [ord('t'), int(data["throttle"])]
        self.i2c_bus.write_i2c_block_data(self.arduino_i2c_addr,0,data)
        # senf the steering angle next
        data = [ord('s'), int(data["steer"])]
        self.i2c_bus.write_i2c_block_data(self.arduino_i2c_addr,0,data)