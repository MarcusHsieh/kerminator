# System Imports
import time
import smbus2
import cv2
import numpy as np
from yoloface import face_analysis
from multiprocessing import Process
import threading
import queue
from adafruit_servokit import ServoKit

# Function Imports
from motorFunction import motorInit
from motorFunction import turnRight
from motorFunction import turnLeft
from motorFunction import stopMotor
from cameraFeed import streamInit


kit = ServoKit(channels=16)
bus = smbus2.SMBus(1)

face = face_analysis()
result_queue = queue.Queue()


def streamStart():
    streamInit()

def detect_faces(frame):
    # Run face detection
    _, box, conf = face.face_detection(frame_arr=frame, frame_status=True, model='tiny')
    result_queue.put(box)

def cameraIntake():
    time.sleep(10)
    cap = cv2.VideoCapture("http://10.42.0.100:7123/stream.mjpg")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_count = 0

    while(1):
        _, frame = cap.read()
        frame_count += 1

        if not _:
            print("Error: Failed to grab frame.")
            break

        frame_skip = 10 # Process every 5 frames
        print(f"Frame Count: {frame_count}")
        if frame_count % frame_skip == 0:
            detection_thread = threading.Thread(target = detect_faces, args = (frame,))
            detection_thread.start()
            detection_thread.join()


            if not result_queue.empty():
                box = result_queue.get()
                if len(box)>0:
                    # Calculate center coordinates of largest rectangle
                    center = (box[0][0] + int(box[0][2]/2), box[0][1] + int(box[0][3]/2))
                    print(f"Center Coordinates: ({center[0]}, {center[1]}) ")
                    if (center[0] < 213):
                        print("turning Left")
                        turnLeft()
                        time.sleep(0.1667)
                        stopMotor()
                    elif (center[0] > 427):
                        print("turning right")
                        turnRight()
                        time.sleep(0.1667)
                        stopMotor()



def motorSpin():


    motorInit()

    kit.servo[15].angle(0)
    time(1)
    kit.servo[15].angle(180)
    time(1)
    kit.servo[15].angle(0)
    time(1)

    # turnLeft()
    # time.sleep(3)
    # turnRight()
    # time.sleep(3)
    stopMotor()
    print("Motor Running")

if __name__ == '__main__':
    streamProcess = Process(target = streamStart)
    cameraProcess = Process(target = cameraIntake)
    motorProcess = Process(target = motorSpin)

    streamProcess.start()
    cameraProcess.start()
    motorProcess.start()

    streamProcess.join()
    cameraProcess.join()
    motorProcess.join()