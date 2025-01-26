import time
import smbus2
from adafruit_motor import servo
from adafruit_servokit import ServoKit
import board
import busio
from adafruit_pca9685 import PCA9685

  # Assuming you're still using SMBus for motor control


def motorInit():
    bus = smbus2.SMBus(1)
    bus.write_byte_data(0x40, 0x00, 0x10)
    bus.write_byte_data(0x40, 0xfe, 0x7E)
    bus.write_byte_data(0x40, 0x00, 0x00)
    bus.write_byte_data(0x40, 0x01, 0x04)
    bus.close()

def turnLeft():
    bus = smbus2.SMBus(1)
    bus.write_byte_data(0x40, 0x08, 0xCC)  # PWM 01 full fwd LSB is 98 measured
    bus.write_byte_data(0x40, 0x09, 0x01)  # PWM 01 full fwd MSB is 01 measured
    time.sleep(0.01667)
    bus.close()

def turnRight():
    bus = smbus2.SMBus(1)
    bus.write_byte_data(0x40, 0x08, 0xCC)  # PWM 01 full fwd LSB is 98 measured
    bus.write_byte_data(0x40, 0x09, 0x00)  # PWM 01 full fwd MSB is 01 measured
    time.sleep(0.01667)
    bus.close()

def stopMotor():
    bus = smbus2.SMBus(1)
    bus.write_byte_data(0x40, 0x08, 0x00)  # PWM 01 off LSB is 32 measured
    bus.write_byte_data(0x40, 0x09, 0x00)  # PWM 01 off MSB is 01 measured
    bus.close()

def servosInit():
    print("Running servos")
    # Create servo instances


def main():
    motorInit()
    turnLeft()
    time.sleep(3)
    turnRight()
    time.sleep(3)
    stopMotor()
    


    # Initialize and control servos
    i2c = board.I2C()  # Setup I2C for PCA9685
    pca = PCA9685(i2c)
    pca.frequency = 50

    servo14 = servo.Servo(pca.channels[14])
    servo15 = servo.Servo(pca.channels[15])

    # Run servo motion
    for i in range(90):
        servo14.angle = 90 - i
        servo15.angle = i
        time.sleep(0.03)
    for i in range(90):
        servo14.angle = i
        servo15.angle = 90 - i
        time.sleep(0.03)


if __name__ == '__main__':
    main()
