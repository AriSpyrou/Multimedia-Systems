import cv2

vid = cv2.VideoCapture('input2.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('input2.avi', fourcc, int(vid.get(5)), (int(vid.get(3)), int(vid.get(4))), False)
while vid.isOpened():
    ret, frame = vid.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out.write(frame)

vid.release()
out.release()
