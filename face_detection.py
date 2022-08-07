from face_lib import face_lib
import pyfakewebcam
import numpy as np
import time
FL = face_lib()
import cv2
import psutil

def average_fps(arr):
    sum = 0
    count = 0
    for fps in arr:
        sum += fps
        count += 1
    return sum/count

#capture video in /dev/video3
vid = cv2.VideoCapture("udp://192.168.122.48:5000?pkt_size=1316",cv2.CAP_FFMPEG)
#set font and WxH video
font = cv2.FONT_HERSHEY_DUPLEX
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT) 
#set up fakecamera 
#change host at (/dev/video5)
cam = pyfakewebcam.FakeWebcam('/dev/video5',int(width), int(height))
#set up value to caculate
sum_frame = 0
sum_face_true = 0
sum_cpu = 0
print_fps_period = 1
frame_count = 0
arr = []
t0 = time.monotonic()
print("Live camera in /dev/video4")

while(vid.isOpened()):
    ret, frame = vid.read()
    if ret == False:
        break
    #facelocation handle 
    #no_of_faces returdp://192.168.122.48:5000?pkt_size=1316",cv2.CAP_FFMPEG)
#set font and WxH video number of faces in frame
    #face_coors return location of face
    no_of_faces, faces_coors = FL.faces_locations(frame)
    if no_of_faces == 1:
        sum_face_true += 1
    #set up value of rectangle
    for val in faces_coors:
        q1 = (val[0], val[1])
        q2 = (val[0] + val[2], val[1] + val[3])
        # draw rectangle
        cv2.rectangle(frame, q1, q2, (0, 0, 255), 2)
    #print number of face in frame
    cv2.putText(frame,str(no_of_faces),(25,25), font, 1.0, (255,255,255), 1)
    #cpu calculate
    cpu = psutil.cpu_percent()
    sum_cpu+=cpu
    #fake camera funtinon
    # cam.schedule_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #cv2 show
    cv2.imshow("frame",frame)
    #fps calculate
    sum_frame += 1
    frame_count += 1
    td = time.monotonic() - t0
    if td > print_fps_period:
        current_fps = frame_count / td
        arr += [current_fps]
        print("FPS: {:6.2f}".format(current_fps), end="\r")
        frame_count = 0
        t0 = time.monotonic()
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#accuracy calculate
face_detection_rate = (sum_face_true/sum_frame)*100
print("face detection rate: {:6.2f}".format(face_detection_rate),"%")
print("FPS: ",average_fps(arr))
print("CPU: ",sum_cpu/sum_frame)
print("Sum frame: ",sum_frame)
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
# cam.print_capabilities()
