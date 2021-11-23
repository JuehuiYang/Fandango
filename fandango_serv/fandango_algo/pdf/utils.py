from PIL import Image
import cv2
import numpy as np


def pixmap2array(pix):
    '''pixmap数据转数组对象'''
    # 获取颜色空间
    cspace = pix.colorspace
    if cspace is None:
        mode = "L"
    elif cspace.n == 1:
        mode = "L" if pix.alpha == 0 else "LA"
    elif cspace.n == 3:
        mode = "RGB" if pix.alpha == 0 else "RGBA"
    else:
        mode = "CMYK"

    # 将byte数据转化为PIL格式
    img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
    # 将PIL转化为numpy格式，并将RGB颜色空间转化为BGR
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    return img


import fitz
from fitz import Pixmap


def array2pix(img):
    height, width, _ = img.shape
    # for i in range(height):
    #     for j in range(width):
    #         # one pixel (some fun coloring)
    #         img[i, j] = [(i + j) % 256, i % 256, j % 256]
    samples = bytearray(img.tostring())
    pix = fitz.Pixmap(fitz.csRGB, width, height, samples)
    return pix
    # return pix


import numpy as np
import fitz
# ==============================================================================
# create a fun-colored width * height PNG with fitz and numpy
# ==============================================================================
# height = 150
# width  = 100
# bild = np.ndarray((height, width, 3), dtype=np.uint8)
#
# for i in range(height):
#     for j in range(width):
#         # one pixel (some fun coloring)
#         bild[i, j] = [(i+j)%256, i%256, j%256]
#
# samples = bytearray(bild.tostring())    # get plain pixel data from numpy array
# pix = fitz.Pixmap(fitz.csRGB, width, height, samples)
# pix.save("test.png")
