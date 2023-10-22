import socket
from PIL import Image 
import numpy as np
import binascii
import re

HOST = "10.100.20.70"  # The server's hostname or IP address
PORT = 7  # The port used by the server
IMG_HEIGHT = 240
IMG_WIDTH = 240
DATA_8bit = IMG_HEIGHT * IMG_WIDTH

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"else")
    data = s.recv(DATA_8bit * 2)

b = bytearray(data)
test  = binascii.hexlify(b)
out = str(test, 'UTF-8')
raw_list = re.findall('....', out)

regex_pattern = r"(..)(..)"
# print((raw_list[0]))

full_img = []

# rgb8bit-RGB332
# for i in range(IMG_HEIGHT):
#     img_line = []
#     for j in range(IMG_WIDTH):
#         img = int(raw_list[i*IMG_HEIGHT + j], 16)
#         r = (img >> 5) / 7.0 * 255.99
#         g = ((img & 0x1c) >> 2) / 7.0 * 255.99
#         b = (img & 0x3) / 3.0 * 255.99
#         img_line.append([r, g, b])
#     full_img.append(img_line)

# rgb16bit-RGB565
for i in range(IMG_HEIGHT):
    img_line = []
    for j in range(IMG_WIDTH):
        img_str = raw_list[i*IMG_HEIGHT + j]
        res = re.sub(regex_pattern, r"\2\1", img_str)
        img = int(res, 16)
        r = (img >> 11) / 31.0 * 255.99
        g = ((img & 0x7E0) >> 5) / 63.0 * 255.99
        b = (img & 0x1F) / 31.0 * 255.99
        img_line.append([r, g, b])
    full_img.append(img_line)


rgb = np.array(full_img, dtype="uint8")
im = Image.fromarray(rgb.astype(np.uint8))
# im.save("zoom.png")
im.show()