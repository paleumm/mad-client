import sys
import numpy as np
import socket
import binascii
import re

from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

HOST = "10.100.20.70"
PORT = 7
IMG_HEIGHT = 240
IMG_WIDTH = 240
DATA = IMG_HEIGHT * IMG_WIDTH
regex_pattern = r"(..)(..)"

class TCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None

    def send_request(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_ip, self.server_port))
            s.sendall(b"get_img")
            data = s.recv(DATA * 2)

        b = bytearray(data)
        test  = binascii.hexlify(b)
        out = str(test, 'UTF-8')
        raw_list = re.findall('....', out)
        full_img = []
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

        return rgb

    def close(self):
        self.client_socket.close()


class MADClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 320, 320)

        self.initUI()
        self.image = None
        self.tcpclient = TCPClient(HOST, PORT)

    def initUI(self):
        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create a layout for the main widget
        main_layout = QVBoxLayout()

        top_button_layout = QHBoxLayout()

        # Create a button to load an image from a NumPy array
        load_button = QPushButton("load image")
        load_button.clicked.connect(self.load_image)
        top_button_layout.addWidget(load_button)

        save_button = QPushButton("save image")
        save_button.clicked.connect(self.save_image)
        top_button_layout.addWidget(save_button)

        main_layout.addLayout(top_button_layout)

        # Create a label to display the image
        self.image_label = QLabel()
        main_layout.addWidget(self.image_label)

        main_widget.setLayout(main_layout)

    def load_image(self):
        # Example NumPy array (you can replace this with your own image data)
        # In this example, we create a simple red square image
        width, height = 240, 240
        # print("requested")
        self.image = self.tcpclient.send_request()
        # print("received")

        # Create a QImage from the NumPy array
        q_image = QImage(
            self.image.data, width, height, 3 * width, QImage.Format.Format_RGB888
        )

        # Create a QPixmap from the QImage and display it
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def save_image(self):
        im = Image.fromarray(self.image)
        im.save("image.jpeg")


def main():
    app = QApplication(sys.argv)
    window = MADClient()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
