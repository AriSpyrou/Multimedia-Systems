import cv2

VIDEO_NAME = 'input'
VIDEO_TYPE = '.avi'
FRAME_SAVE_DEST = 'frames/'
f_cnt = 1


vid = cv2.VideoCapture(VIDEO_NAME + VIDEO_TYPE)
while vid.isOpened():
    ret, c_frame = vid.read()
    if not ret:
        break
    c_frame = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(FRAME_SAVE_DEST + 'frame_' + str(f_cnt) + '.bmp', c_frame)
    f_cnt += 1

vid.release()
