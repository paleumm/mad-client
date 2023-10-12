import sys
import numpy as np
import socket
import io
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

class TCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"Connection error: {e}")
            self.client_socket.close()

    def send_request(self, request_message):
        try:
            self.client_socket.send(request_message.encode())
        except Exception as e:
            print(f"Error sending request: {e}")

    def receive_bitmap(self):
        try:
            # Read the size of the incoming image
            image_size_bytes = self.client_socket.recv(1)
            image_size = int.from_bytes(image_size_bytes, byteorder='big')

            # Receive the image data
            image_data = b""
            while len(image_data) < image_size:
                chunk = self.client_socket.recv(image_size - len(image_data))
                if not chunk:
                    break
                image_data += chunk

            # Convert image data to a NumPy array
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)

            return image_array
        except Exception as e:
            print(f"Error receiving bitmap: {e}")
            return None

    def close(self):
        self.client_socket.close()


class MADClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 320, 320)

        self.initUI()
        self.image = None
        self.tcpclient = TCPClient("10.100.0.180", 10)

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
        # image_data = np.zeros((height, width, 3), dtype=np.uint8)
        # image_data[:, :] = [255, 0, 0]  # Red color
        self.tcpclient.connect()
        self.tcpclient.send_request("get")
        print("requested")
        self.image = self.tcpclient.receive_bitmap()
        print("received")
        print(self.image)
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
