import time
import smbus2
from adafruit_servokit import ServoKit
from motorFunction import motorInit
from motorFunction import turnRight
from motorFunction import turnLeft
from motorFunction import stopMotor
from cameraFeed import cameraInit

bus = smbus2.SMBus(1)

def run():
    cameraInit()
    motorInit()
    for i in range(1):
        turnLeft()
        time.sleep(3)
        turnRight()
        time.sleep(3)
    stopMotor()
    print("Motor Running")

if __name__ == '__main__':
    print("Running main")
    run()