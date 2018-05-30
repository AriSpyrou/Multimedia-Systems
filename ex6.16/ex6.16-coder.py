from PIL import Image
import numpy as np

Q_PARAMETER = 10
IMAGE_PATH = '../images/'
IMAGE_NAME = 'gimg1'
IMAGE_TYPE = '.bmp'


img = np.array(Image.open(IMAGE_PATH + IMAGE_NAME + IMAGE_TYPE).convert('L'))
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
file = open('compressed_' + IMAGE_NAME, 'w')
file.write(output)
file.close()
