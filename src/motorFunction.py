import time
import smbus2
from adafruit_servokit import ServoKit
bus = smbus2.SMBus(1)

def motorInit():
    bus.write_byte_data(0x40, 0x00, 0x10)
    bus.write_byte_data(0x40, 0xfe, 0x7E)
    bus.write_byte_data(0x40, 0x00, 0x00)
    bus.write_byte_data(0x40, 0x01, 0x04)

def turnLeft():
    bus.write_byte_data(0x40,0x06,0x00)  # PWM 01 config
    bus.write_byte_data(0x40,0x07,0x00)  # PWM 01 config
    bus.write_byte_data(0x40,0x08,0x98)  # PWM 01 full fwd LSB is 98 measured
    bus.write_byte_data(0x40,0x09,0x01)  # PWM 01 full fwd MSB is 01 measured
    # time.sleep(0.05)

def turnRight():
    bus.write_byte_data(0x40,0x06,0x00)  # PWM 01 config
    bus.write_byte_data(0x40,0x07,0x00)  # PWM 01 config
    bus.write_byte_data(0x40,0x08,0xCC)  # PWM 01 full fwd LSB is 98 measured
    bus.write_byte_data(0x40,0x09,0x00)  # PWM 01 full fwd MSB is 01 measured
    # time.sleep(0.05) # Moves for 0.05 seconds

def stopMotor():
    bus.write_byte_data(0x40,0x06,0x00)  # PWM 01 config
    bus.write_byte_data(0x40,0x07,0x00)  # PWM 01 config
    bus.write_byte_data(0x40,0x08,0x32)  # PWM 01 off LSB is 32 measured
    bus.write_byte_data(0x40,0x09,0x01)  # PWM 01 off MSB is 01 measured