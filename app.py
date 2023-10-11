import sys
import numpy as np
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout

class MADClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 320, 320)

        self.initUI()
        self.image = None

    def initUI(self):
        # Create the main widget and set it as the central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create a layout for the main widget
        main_layout = QVBoxLayout()

        top_button_layout = QHBoxLayout()

        # Create a button to load an image from a NumPy array
        load_button = QPushButton("load image")
        load_button.clicked.connect(self.load_image_from_numpy_array)
        top_button_layout.addWidget(load_button)

        save_button = QPushButton("save image")
        save_button.clicked.connect(self.save_image)
        top_button_layout.addWidget(save_button)

        main_layout.addLayout(top_button_layout)

        # Create a label to display the image
        self.image_label = QLabel()
        main_layout.addWidget(self.image_label)


        main_widget.setLayout(main_layout)

    def load_image_from_numpy_array(self):
        # Example NumPy array (you can replace this with your own image data)
        # In this example, we create a simple red square image
        width, height = 240, 240
        image_data = np.zeros((height, width, 3), dtype=np.uint8)
        image_data[:, :] = [255, 0, 0]  # Red color

        self.image = image_data

        # Create a QImage from the NumPy array
        q_image = QImage(image_data.data, width, height, 3 * width, QImage.Format.Format_RGB888)

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