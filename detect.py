import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time

import cv2

fullbody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cars_cascade = cv2.CascadeClassifier('cars.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
    help="path to input video file")
args = vars(ap.parse_args())

if not args.get("video", False):
	print("[INFO] starting video stream...")
	cap = VideoStream(src=0).start()
	time.sleep(1.0)
else:
     cap=cv2.VideoCapture(args["video"])
     if not cap.isOpened():
        print("Error!")
        exit()

count=0

while True:
    frame=cap.read() #ret=> boolean, 0 if frames not loaded,  1 if frames loaded
    
    frame=frame[1] if args.get("video", False) else frame

    if frame is None:
        break

    
    height,width,layers= frame.shape
    newh=height/2
    neww=width/2

    count=count+1

    if args.get("video", False):
        frame=cv2.resize(frame,(int(neww),int(newh)))
    else:
        frame=cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    bodies = fullbody_cascade.detectMultiScale(gray)

    for (x, y, w, h) in bodies:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cars = cars_cascade.detectMultiScale(gray)

    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

     

    cv2.imshow('Full-Body Detection', frame)

    
    if cv2.waitKey(25) & 0xFF == ord('u'):
        break

if not args.get("video", False):
    cap.stop()
else:
    cap.release()


cv2.destroyAllWindows()
    