from PIL import Image
import numpy as np

PATH = './compressed_'
NAME = 'gimg1'


buf = open(PATH + NAME, 'r').read()
buf = buf.split('|', 2)
DIMENSIONS = buf[0].split('x')
DIMENSIONS[0] = int(DIMENSIONS[0])
DIMENSIONS[1] = int(DIMENSIONS[1])
Q_PARAMETER = int(buf[1])
img_array = np.empty((int(DIMENSIONS[0]), int(DIMENSIONS[1])), dtype=int)
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
rec_img = Image.fromarray(img_array)
rec_img.show()
