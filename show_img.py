import numpy as np
from PIL import Image

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, help="input file")
args = vars(parser.parse_args())

filename = args["file"]

file = open(filename, 'r')

lines = file.readlines()

full_img = []

i = 0
for line in lines:
    img_line = []
    for pixel in line.split(' '):
        if pixel == '\n' or pixel == '':
            continue
        img = int(pixel, 16)
        r = (img >> 5) / 7.0 * 255.99
        g = ((img & 0x1c) >> 2) / 7.0 * 255.99
        b = (img & 0x3) / 3.0 * 255.99
        img_line.append([r, g, b])
    full_img.append(img_line)

rgb = np.array(full_img, dtype="uint8")

print(rgb.shape)

im = Image.fromarray(rgb.astype(np.uint8))
# im.save("zoom.png")
im.show()