import numpy as np
import cv2
import time

# Program parameters
MACROBLOCK_SIZE = 16
K = 16

# Variables meant for output purposes
start = time.time()
frames = 1


def mean_squared_error(alpha, beta):  # MSE metric (not used)
    mse = 0
    n = alpha.shape[0]
    for i in range(n):
        for j in range(n):
            mse += (alpha[i, j] - beta[i, j]) ** 2
    return mse * (n ** -2)


def sum_absolute_differences(alpha, beta):  # SAD metric
    sad = 0
    n = alpha.shape[0]
    for i in range(n):
        for j in range(n):
            sad += abs(int(alpha[i, j]) - int(beta[i, j]))
    return sad


# Adds padding to each frame which is needed to
def fix_frame_shape(frame):
    return np.pad(frame, ((0, int((np.ceil(vid.get(4)/MACROBLOCK_SIZE) * MACROBLOCK_SIZE) - vid.get(4))),
                          (0, int((np.ceil(vid.get(3)/MACROBLOCK_SIZE) * MACROBLOCK_SIZE) - vid.get(3)))),
                  'constant', constant_values=0)


def compute_motion_vector(macroblock, ref, crds):
    m = [0, K/2, -K/2]
    best = sum_absolute_differences(macroblock, ref[crds[0]:crds[0] + MACROBLOCK_SIZE, crds[1]:crds[1] + MACROBLOCK_SIZE])
    best_i = crds
    while True:
        for i in range(len(m)):
            for j in range(len(m)):
                if m[i] == m[j] == 0:
                    continue
                try:
                    temp = sum_absolute_differences(macroblock,
                                                    ref[int(best_i[0] + m[i]):int(best_i[0] + MACROBLOCK_SIZE + m[i]),
                                                        int(best_i[1] + m[j]):int(best_i[1] + MACROBLOCK_SIZE + m[j])])
                    if temp < best:
                        best = temp
                        best_i = (best_i[0] + m[i], best_i[1] + m[j])
                except IndexError:
                    pass
        m[:] = [x / 2 for x in m]
        if m[1] < 1:
            break
    return tuple(np.subtract(best_i, crds, dtype=int, casting='unsafe'))


# Open the video and read the first frame which will be used as the background
vid = cv2.VideoCapture('input.mp4')
ret, bg_f = vid.read()
bg_f = cv2.cvtColor(bg_f, cv2.COLOR_BGR2GRAY)
# Initialize the video writer and write the background frame
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('m' + str(MACROBLOCK_SIZE) + 'k' + str(K) + '.avi', fourcc, vid.get(5),
                      (int(vid.get(3)), int(vid.get(4))), False)
out.write(bg_f)
bg_f = fix_frame_shape(bg_f)

r_frame = bg_f
while vid.isOpened():
    ret, c_frame = vid.read()
    if not ret:
        break
    c_frame = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
    c_frame = fix_frame_shape(c_frame)
    for i in range(0, c_frame.shape[0], MACROBLOCK_SIZE):
        for j in range(0, c_frame.shape[1], MACROBLOCK_SIZE):
            motion_v = compute_motion_vector(c_frame[i:i+MACROBLOCK_SIZE, j:j+MACROBLOCK_SIZE], r_frame, (i, j))
            if motion_v[0] + motion_v[1] != 0:
                c_frame[i:i+MACROBLOCK_SIZE, j:j+MACROBLOCK_SIZE] = bg_f[i:i+MACROBLOCK_SIZE, j:j+MACROBLOCK_SIZE]
    r_frame = c_frame
    c_frame = np.delete(c_frame, slice(int(vid.get(4)), None), 0)
    c_frame = np.delete(c_frame, slice(int(vid.get(3)), None), 1)
    out.write(c_frame)
    ########
    frames += 1
    print('Frames Processed: ' + str(frames))
    ########

vid.release()
out.release()
print('-----' + str(time.time()-start) + '-----')
