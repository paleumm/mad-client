import socket
import io
from PIL import Image 
import numpy as np
import struct
import binascii
import re

HOST = "192.168.1.70"  # The server's hostname or IP address
PORT = 7  # The port used by the server
IMG_HEIGHT = 240
IMG_WIDTH = 240

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"else")
    data = s.recv(240*240)

# image = Image.open(io.BytesIO(data))
# image_array = np.array(image)
# print(f"Received {data!r}")

b = bytearray(data)
test  = binascii.hexlify(b)
# print(test)
out = str(test, 'ascii')

raw_list = re.findall('.{1,2}', out)

print(len(raw_list))
full_img = []
for i in range(IMG_HEIGHT):
    img_line = []
    for j in range(IMG_WIDTH):
        img = int(raw_list[i*IMG_HEIGHT + j], 16)
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