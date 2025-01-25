import time
import smbus2
from adafruit_servokit import ServoKit
from motorFunction import motorInit
from motorFunction import turnRight
from motorFunction import stopMotor

bus = smbus2.SMBus(1)

def run():
    motorInit()
    for i in range(1):
        turnRight()
    stopMotor()
    print("Motor Running")

if __name__ == '__main__':
    print("Running main")
    run()