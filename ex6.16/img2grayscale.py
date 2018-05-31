from PIL import Image

_IMAGE_DICT = {'jpg': 'JPEG',
               'bmp': 'BMP'}

IMAGE_PATH = '../images/'
IMAGE_NAME = 'img3'
IMAGE_NEW_NAME = 'g' + IMAGE_NAME
IMAGE_TYPE = 'bmp'
OVERWRITE = False

if OVERWRITE:
    Image.open(IMAGE_PATH + IMAGE_NAME + '.' + IMAGE_TYPE).convert('L').save(
        IMAGE_PATH +
        IMAGE_NAME + '.' +
        IMAGE_TYPE, _IMAGE_DICT[IMAGE_TYPE])
else:
    Image.open(IMAGE_PATH + IMAGE_NAME + '.' + IMAGE_TYPE).convert('L').save(
        IMAGE_PATH +
        IMAGE_NEW_NAME + '.' +
        IMAGE_TYPE, _IMAGE_DICT[IMAGE_TYPE])
