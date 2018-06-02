import numpy as np
import cv2
import time

PATH = 'compressed_frames/'
NAME = 'compressed_frame_'
N_FRAMES = 60


start = time.time()
readfile = open(PATH + NAME + str(1), 'r').read()
readfile = readfile.split('|', 2)
size = readfile[0].split('x')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('out.avi', fourcc, 30.0, (int(size[1]), int(size[0])), False)

for frames in range(1, N_FRAMES + 1):
    buf = open(PATH + NAME + str(frames), 'r').read()
    buf = buf.split('|', 2)
    DIMENSIONS = buf[0].split('x')
    DIMENSIONS[0] = int(DIMENSIONS[0])
    DIMENSIONS[1] = int(DIMENSIONS[1])
    Q_PARAMETER = int(buf[1])
    img_array = np.empty((int(DIMENSIONS[0]), int(DIMENSIONS[1])), dtype=np.uint8)
    buf = buf[2].split(';', 1)
    if ',' in buf[0]:
        run_length = buf[0].split(',')
        run_length[0] = int(run_length[0])
        run_length[1] = int(run_length[1])
    else:
        run_length = [0, 1]
        run_length[0] = int(buf[0])
    for i in range(DIMENSIONS[0]):
        for j in range(DIMENSIONS[1]):
            if run_length[1] > 0:
                if run_length[0] * Q_PARAMETER <= 255:
                    img_array[i, j] = run_length[0] * Q_PARAMETER
                else:
                    img_array[i, j] = 255
                run_length[1] -= 1
            else:
                if buf[1] != '':
                    buf = buf[1].split(';', 1)
                    if ',' in buf[0]:
                        run_length = buf[0].split(',')
                        run_length[0] = int(run_length[0])
                        run_length[1] = int(run_length[1])
                    else:
                        run_length[0] = int(buf[0])
                        run_length[1] = 1

                    if run_length[0] * Q_PARAMETER <= 255:
                        img_array[i, j] = run_length[0] * Q_PARAMETER
                    else:
                        img_array[i, j] = 255
                    run_length[1] -= 1
                else:
                    break
    frame = img_array
    out.write(img_array)
    print('Frames Processed: ' + str(frames))
print('Time elapsed: ' + str(round((time.time() - start), 2)) + 's')
cv2.destroyAllWindows()
out.release()
