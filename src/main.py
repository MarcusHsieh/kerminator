# System Imports
import time
import smbus2
import cv2
import numpy as np
from multiprocessing import Process
from adafruit_servokit import ServoKit

# Function Imports
from motorFunction import motorInit
from motorFunction import turnRight
from motorFunction import turnLeft
from motorFunction import stopMotor
from cameraFeed import streamInit

bus = smbus2.SMBus(1)

def streamStart():
    streamInit()

def cameraInit():
    time.sleep(10)
    cap = cv2.VideoCapture("http://10.42.0.100:7123/stream.mjpg")
    face_frontal_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    # face_alt1_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt1.xml")

    face_alt2_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    face_alt_tree_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt_tree.xml")
    # face_profle_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while(1):
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to grab frame.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found = face_frontal_classifier.detectMultiScale(gray_frame, minSize = (24, 24), scaleFactor=1.1, minNeighbors=12)
        amount_found = len(found)


        print(f"Amount Found: {amount_found}")
        sorted_rects = sorted(found, key=lambda r: r[2] * r[3], reverse=True)

        if (len(sorted_rects) > 0):
            # Calculate center coordinates of largest rectangle
            center = (sorted_rects[0][0] + int(sorted_rects[0][2]/2), sorted_rects[0][1] + int(sorted_rects[0][3]/2))
            print(f"Center Coordinates: ({center[0]}, {center[1]}) ")
            if (center[0] > 500):
                turnLeft()
                time.sleep(0.5)
                stopMotor()
            elif (center[0] < 140):
                turnRight()
                time.sleep(0.5)
                stopMotor()

def motorSpin():
    motorInit()
    for i in range(1):
        turnLeft()
        time.sleep(3)
        turnRight()
        time.sleep(3)
    stopMotor()
    print("Motor Running")

if __name__ == '__main__':
    streamProcess = Process(target = streamStart)
    cameraProcess = Process(target = cameraInit)
    motorProcess = Process(target = motorSpin)

    streamProcess.start()
    cameraProcess.start()
    motorProcess.start()

    streamProcess.join()
    cameraProcess.join()
    motorProcess.join()