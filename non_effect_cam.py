import cv2
import numpy as np
import time
import pyfakewebcam
import psutil
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('2.mp4')
new_frame_time = 1
prev_frame_time = 0
sum_frame = 0
sum_fps = 0
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
else:
  width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
  height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
  #localhost to stream video
  cam = pyfakewebcam.FakeWebcam('/dev/video3',int(width), int(height))
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    # Display the resulting frame
    cam.schedule_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #fps calculate
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    new_frame_time = time.time()
    fps = float(fps)
    sum_fps += fps
    sum_frame += 1
    #delay 1/100 to have 60 fps
    time.sleep(1/40.0)
    print("FPS non effect: {:6.2f}".format(fps),"\tCPU:{:6.2f}".format(psutil.cpu_percent()),end='\r')
    # cv2.imshow("frame",frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break
print("FPS: ",sum_fps/sum_frame)

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()