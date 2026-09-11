import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time

font = cv2.FONT_HERSHEY_SIMPLEX

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
    help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="mil",
    help="OpenCV object tracker type")
args = vars(ap.parse_args())

if not args.get("video", False):
	print("[INFO] starting video stream...")
	cap = VideoStream(src=0).start()
	time.sleep(1.0)
else:
     cap=cv2.VideoCapture(args["video"])

fps=None

# if not cap.isOpened():
#     print("Error!")
#     exit()

count=0 #frame count

OPENCV_OBJECT_TRACKERS = {
    "kcf": cv2.TrackerKCF_create,
    # "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    # "tld": cv2.TrackerTLD_create,
    # "medianflow": cv2.TrackerMedianFlow_create,
    # "mosse": cv2.TrackerMOSSE_create
}

# grab the appropriate object tracker using our dictionary of
# OpenCV object tracker objects
tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

# initialize the bounding box coordinates of the object we are going to track
initBB = None

while True:
    frame=cap.read() #ret=> boolean, 0 if frames not loaded,  1 if frames loaded, frame=(ret,frame)
    
    frame=frame[1] if args.get("video", False) else frame

    if frame is None:
        break
    
    height,width,layers= frame.shape
    newh=height/4.5
    neww=width/4.5

    if args.get("video", False):
        frame=cv2.resize(frame,(int(neww),int(newh)))
    else:
        frame=cv2.flip(frame, 1)

    count=count+1
    
    # cv2.putText(resize, 
    #             f"Frame count = {count}", 
    #             (200, 200), 
    #             font, 1, 
    #             (0, 0, 0), 
    #             2, 
    #             cv2.LINE_4)
    
    if initBB is not None:
		# grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        		# check to see if the tracking was a success
    
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                (0, 255, 0), 2)
        
        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on the frame
        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, int(newh) - ((i * 20) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
    cv2.imshow("My video",frame)


    # show the output frame
    key = cv2.waitKey(1) & 0xFF
    # if the 's' key is selected, we are going to "select" a bounding box to track
    if key == ord("s"):
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
            showCrosshair=False)
        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)
        fps = FPS().start()
        cv2.destroyWindow("Frame")

        # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break
    # if we are using a webcam, release the pointer
if not args.get("video", False):
    cap.stop()
# otherwise, release the file pointer
else:
    cap.release()


cv2.destroyAllWindows()
    