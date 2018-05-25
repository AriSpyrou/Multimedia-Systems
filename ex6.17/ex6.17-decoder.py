import cv2

Q_PARAMETER = 10

vid = cv2.VideoCapture('quantized.avi')
ret, first_frame = vid.read()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (790, 834))
out.write(first_frame)

prev_frame = first_frame

while vid.isOpened():
    ret, c_frame = vid.read()
    if not ret:
        break
    # c_frame = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
    c_frame = (c_frame * Q_PARAMETER) + prev_frame
    prev_frame = c_frame
    out.write(c_frame)

vid.release()
out.release()

