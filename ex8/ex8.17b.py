import numpy as np
import cv2
import time

# Program parameters
MACROBLOCK_SIZE = 16
K = 16
PLAYBACK = True

# Variables meant for output purposes
start = time.time()
frames = 1


def sum_absolute_differences(alpha, beta):  # SAD metric
    sad = 0
    n = alpha.shape[0]
    for i in range(n):
        for j in range(n):
            sad += abs(int(alpha[i, j]) - int(beta[i, j]))
    return sad


# Adds padding to each frame which is needed so that the dimensions are divisible by the size of the macroblock
def fix_frame_shape(frame):
    return np.pad(frame, ((0, int((np.ceil(vid.get(4)/MACROBLOCK_SIZE) * MACROBLOCK_SIZE) - vid.get(4))),
                          (0, int((np.ceil(vid.get(3)/MACROBLOCK_SIZE) * MACROBLOCK_SIZE) - vid.get(3)))),
                  'constant', constant_values=0)


def compute_motion_vector(macroblock, ref, crds):  # Computes the motion vector using the logarithmic search method
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
# Initialize the video writer and write the background frame
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('8-17b.avi', fourcc, vid.get(5),
                      (int(vid.get(3)), int(vid.get(4))), False)
ret, r_frame = vid.read()
r_frame = fix_frame_shape(cv2.cvtColor(r_frame, cv2.COLOR_BGR2GRAY))
while vid.isOpened():
    ret, c_frame = vid.read()
    if not ret:
        break
    c_frame = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
    c_frame = fix_frame_shape(c_frame)
    temp = np.zeros((r_frame.shape[0], r_frame.shape[1]), dtype=np.uint8)
    for i in range(0, c_frame.shape[0], MACROBLOCK_SIZE):
        for j in range(0, c_frame.shape[1], MACROBLOCK_SIZE):
            motion_v = compute_motion_vector(c_frame[i:i+MACROBLOCK_SIZE, j:j+MACROBLOCK_SIZE], r_frame, (i, j))
            cv2.subtract(c_frame[i:i + MACROBLOCK_SIZE, j:j + MACROBLOCK_SIZE],
                         r_frame[i + motion_v[0]:i + MACROBLOCK_SIZE + motion_v[0],
                                 j + motion_v[1]:j + MACROBLOCK_SIZE + motion_v[1]],
                         temp[i:i+MACROBLOCK_SIZE, j:j+MACROBLOCK_SIZE])
    r_frame = c_frame
    temp = np.delete(temp, slice(int(vid.get(4)), None), 0)
    temp = np.delete(temp, slice(int(vid.get(3)), None), 1)
    out.write(temp)
    frames += 1
    print('Frames Processed: ' + str(frames))

vid.release()
out.release()
print('Time elapsed: ' + str(round(time.time() - start)) + 's')

# If PLAYBACK is set to True once the process is finished the video will play in its totality.
# Otherwise you can also play it with a media player program
if PLAYBACK:
    vid = cv2.VideoCapture('8-17b.avi')
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
