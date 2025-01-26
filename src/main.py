# System Imports
import time
import smbus2
import cv2
import numpy as np
from yoloface import face_analysis
from multiprocessing import Process
import threading
from queue import Queue
from adafruit_servokit import ServoKit

# Function Imports
from motorFunction import motorInit
from motorFunction import turnRight
from motorFunction import turnLeft
from motorFunction import stopMotor
from motorFunction import servoWave
from motorFunction import speak
from cameraFeed import streamInit

face = face_analysis()

# Holds up to 30 frames for computation
frame_queue = Queue(maxsize=30)
# Queue for YOLO detection results
result_queue = Queue() 


def streamStart():
    streamInit()

# Thread for waving
wave = 1
def waving():
    while (1):
        global wave
        if (wave == 1):
            servoWave()
            wave = 0
            break

speakbit = 1
def speakTask():
    global speakbit
    while(1):
        if (speakbit == 1):
            speak()
            speakbit = 0
            break

# Thread for face detection
def detect_faces():
    while(1):
        if not frame_queue.empty():
            frame = frame_queue.get() 
            # Run face detection
            print(f"Running detection")
            _, box, conf = face.face_detection(frame_arr=frame, frame_status=True, model='tiny')
            result_queue.put(box)
        else:
            time.sleep(0.01)

# Thread for sending commands to the neck motor 
def motor_commands():
    skip_frames = 0
    while (1):
        if not result_queue.empty():
            box = result_queue.get()

            # If we need to skip frames
            if skip_frames > 0:
                skip_frames -= 1  # Decrement the skip counter
                print(f"Skipping frame, {skip_frames} left")
                continue  # Skip this iteration
            # Calculate center coordinates of largest rectangle
            if len(box) > 0:
                print(box)
                center = (box[0][0] + int(box[0][2]/2), box[0][1] + int(box[0][3]/2))
                print(f"Center Coordinates: ({center[0]}, {center[1]}) ")
                if (center[0] < 213):
                    print("turning Right")
                    turnRight()
                    time.sleep(0.01667)
                    stopMotor()
                elif (center[0] > 427):
                    print("turning Left")
                    turnLeft()
                    time.sleep(0.01667)
                    stopMotor()
                skip_frames = 10


# Thread for reading input from the streamed camera input
def camera_intake():
    time.sleep(10)
    frameCount = 0
    cap = cv2.VideoCapture("http://10.42.0.100:7123/stream.mjpg")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while(1):
        frameCount += 1
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to grab frame.")
            break
        if frameCount % 10 == 0:
            if not frame_queue.full():
                frame_queue.put(frame)
            else:
                print(f"Frame Queue Full, dropping frame {frameCount}")

# Runs all of the threads
if __name__ == '__main__':
    stopMotor()
    stream_thread = threading.Thread(target = streamStart)
    camera_thread = threading.Thread(target = camera_intake)
    detection_thread = threading.Thread(target = detect_faces)
    result_thread = threading.Thread(target = motor_commands)
    # motor_thread = threading.Thread(target = motorSpin)
    wave_thread = threading.Thread(target = waving)
    # speak_thread = threading.Thread(target = speakTask)

    stream_thread.start()
    camera_thread.start()
    detection_thread.start()
    result_thread.start()
    # motor_thread.start()
    wave_thread.start()
    # speak_thread.start()

    stream_thread.join()
    camera_thread.join()
    detection_thread.join()
    result_thread.join()
    # motor_thread.join()
    wave_thread.join()
    # speak_thread.join()