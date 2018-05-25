import numpy as np
import cv2
import time

# Program parameters
PLAYBACK = False

# Variables meant for output purposes
start = time.time()
frames = 0

# Open the video and read the first frame which will be used as the background
vid = cv2.VideoCapture('input.mp4')
# Initialize the video writer and write the background frame
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('8-17a.avi', fourcc, vid.get(5),
                      (int(vid.get(3)), int(vid.get(4))), False)
ret, r_frame = vid.read()
r_frame = cv2.cvtColor(r_frame, cv2.COLOR_BGR2GRAY)

while vid.isOpened():
    ret, c_frame = vid.read()
    if not ret:
        break
    c_frame = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
    out.write(np.subtract(c_frame, r_frame))
    r_frame = c_frame
    ########
    frames += 1
    print('Frames Processed: ' + str(frames))
    ########

vid.release()
out.release()
print('Time elapsed: ' + str(round((time.time() - start), 2)) + 's')

# If PLAYBACK is set to True once the process is finished the video will play in its totality.
# Otherwise you can also play it with a media player program
if PLAYBACK:
    vid = cv2.VideoCapture('8-17a.avi')
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Video Playback', frame)
        if cv2.waitKey(int(vid.get(5))) & 0xFF == ord('q'):
            break
    vid.read()
    cv2.destroyAllWindows()