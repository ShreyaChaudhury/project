import cv2
font = cv2.FONT_HERSHEY_SIMPLEX
cap=cv2.VideoCapture("video.mp4") 
if not cap.isOpened():
    print("Error!")
    exit()
count=0
while True:
    ret,frame=cap.read() #ret=> boolean, 0 if frames not loaded,  1 if frames loaded
    if(ret==None):
        break
    height,width,layers= frame.shape
    newh=height/4.5
    neww=width/4.5
    resize=cv2.resize(frame,(int(neww),int(newh)))
    count=count+1
    
    cv2.putText(resize, 
                f"Frame count = {count}", 
                (200, 200), 
                font, 1, 
                (0, 0, 0), 
                2, 
                cv2.LINE_4)
    cv2.imshow("My video",resize)
    
    if cv2.waitKey(25) & 0xFF == ord('u'):
        break
cap.release()
cv2.destroyAllWindows()
    