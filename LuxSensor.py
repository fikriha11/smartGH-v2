import smbus
import time


def readLux():
    try:
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        lux = data[1] * 256 + data[0]
        return lux
    except Exception as error:
        print(error)
