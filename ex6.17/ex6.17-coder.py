import cv2

Q_PARAMETER = 10

frames = 1


vid = cv2.VideoCapture('input.mp4')
ret, first_frame = vid.read()
first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)  # first frame is passed as it is

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('quantized.avi', fourcc, int(vid.get(5)), (int(vid.get(3)), int(vid.get(4))), False)
out.write(first_frame)

prev_frame = first_frame
while vid.isOpened():
    ret, c_frame = vid.read()
    if not ret:
        break
    c_frame = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
    diff = c_frame - prev_frame
    Q_diff = diff//Q_PARAMETER  # divide rounded
    prev_frame = c_frame

    frames += 1
    print(diff, frames)
    print(Q_diff, frames)
    out.write(Q_diff)

vid.release()
out.release()
