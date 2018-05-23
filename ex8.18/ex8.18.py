import numpy as np
import cv2

MACROBLOCK_SIZE = 16


def mean_squared_error(alpha, beta):
    mse = 0
    n = alpha.shape[0]
    for i in range(n):
        for j in range(n):
            mse += (alpha[i, j] - beta[i, j]) ** 2
    return mse * (n ** -2)


def sum_absolute_differences(alpha, beta):
    sad = 0
    n = alpha.shape[0]
    for i in range(n):
        for j in range(n):
            sad += abs(alpha[i, j] - beta[i, j])
    return sad


def fix_frame_shape(frame):
    return np.pad(frame, ((0, int((np.ceil(vid.get(4)/MACROBLOCK_SIZE) * MACROBLOCK_SIZE) - vid.get(4))),
                          (0, int((np.ceil(vid.get(3)/MACROBLOCK_SIZE) * MACROBLOCK_SIZE) - vid.get(3)))),
                  'constant', constant_values=0)


def compute_motion_vector(macroblock, reference):
    print('o')


# Open the video and read the first frame which will be used as the background
vid = cv2.VideoCapture('input.mp4')
ret, bg_f = vid.read()
bg_f = cv2.cvtColor(bg_f, cv2.COLOR_BGR2GRAY)
# Initialize the video writer and write the background frame
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, vid.get(5), (vid.get(3), vid.get(4)), False)
out.write(bg_f)
bg_f = fix_frame_shape(bg_f)


r_frame = bg_f
while vid.isOpened():
    ret, c_frame = vid.read()
    if not ret:
        break
    c_frame = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
    for i in range(0, c_frame.shape[0], MACROBLOCK_SIZE):
        for j in range(0, c_frame.shape[1], MACROBLOCK_SIZE):
            compute_motion_vector(c_frame[i:MACROBLOCK_SIZE, j:MACROBLOCK_SIZE], r_frame)

vid.release()
out.release()
cv2.destroyAllWindows()
