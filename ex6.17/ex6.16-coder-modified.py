from PIL import Image
import numpy as np
import time

Q_PARAMETER = 10
N_FRAMES = 60
IMAGE_PATH = 'frames/'
DEST_PATH = 'compressed_frames/'
IMAGE_NAME = 'frame_'
IMAGE_TYPE = '.bmp'


start = time.time()
for frames in range(1, N_FRAMES + 1):
    img = np.array(Image.open(IMAGE_PATH + IMAGE_NAME + str(frames) + IMAGE_TYPE).convert('L'))
    img[0, 0] = int(round(img[0, 0] / Q_PARAMETER))
    start_flag = True
    run = img[0, 0]
    length = 1
    output = str(img.shape[0]) + 'x' + str(img.shape[1]) + '|' + str(Q_PARAMETER) + '|'
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if start_flag:
                start_flag = False
                continue
            img[i, j] = int(round(img[i, j] / Q_PARAMETER))
            if img[i, j] != run:
                if length != 1:
                    output += str(run) + ',' + str(length) + ';'
                    run = img[i, j]
                    length = 1
                else:
                    output += str(run) + ';'
                    run = img[i, j]
            else:
                length += 1
    if length != 1:
        output += str(run) + ',' + str(length) + ';'
    else:
        output += str(run) + ';'
    print('Frames Processed: ' + str(frames))
    file = open(DEST_PATH + 'compressed_' + IMAGE_NAME + str(frames), 'w')
    file.write(output)
    file.close()
print('Time elapsed: ' + str(round((time.time() - start), 2)) + 's')
