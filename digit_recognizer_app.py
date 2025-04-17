import sys
import os
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox
)
from PyQt5.QtGui import QImage, QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt
from tensorflow.keras.models import load_model
from PIL import Image


class DigitRecognizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Fun Digit Recognizer for Kids 🎨")
        self.setGeometry(100, 100, 400, 500)

        self.model = None
        self.load_model("digit_recognizer.h5")  # Load the model at startup

        self.canvas = DrawingCanvas(self)
        self.predict_button = self.create_button("🎯 Predict Digit 🎯", self.predict_digit, "#FFDD59")
        self.clear_button = self.create_button("🧹 Clear Canvas 🧹", self.clear_canvas, "#FF6B6B")

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.clear_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_button(self, text, callback, color):
        """Creates a custom button with a kid-friendly design."""
        button = QPushButton(text, self)
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color};
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                color: #FFF;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #FFC312;
            }}
            """
        )
        button.clicked.connect(callback)
        return button

    def load_model(self, model_path):
        """Loads the trained model."""
        if os.path.exists(model_path):
            try:
                self.model = load_model(model_path)
                print(f"Model loaded successfully from '{model_path}'.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load model:\n{e}")
                sys.exit(1)
        else:
            QMessageBox.critical(self, "Error", f"Model file '{model_path}' not found.")
            sys.exit(1)

    def predict_digit(self):
        """Predicts the digit drawn on the canvas."""
        if not self.model:
            QMessageBox.warning(self, "Error", "Model is not loaded.")
            return

        # Get the image from the canvas
        image = self.canvas.get_image()
        # Resize to 28x28 (MNIST format)
        image = image.resize((28, 28)).convert('L')
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        image_array = image_array.reshape(1, 28, 28, 1)  # Add batch and channel dimensions

        # Predict the digit
        prediction = self.model.predict(image_array)
        predicted_digit = np.argmax(prediction)
        confidence = prediction[0][predicted_digit]

        # Display the result in the title bar
        self.setWindowTitle(f"🎉 Predicted: {predicted_digit} (Confidence: {confidence:.2f}) 🎉")

    def clear_canvas(self):
        """Clears the canvas."""
        self.canvas.clear()


class DrawingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 300)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.last_point = None

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing and self.last_point is not None:
            painter = QPainter(self.image)
            pen = QPen(Qt.black, 15, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            pen.setColor(QColor("#1E90FF"))  # Fun blue color for drawing
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.last_point = None

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def get_image(self):
        """Returns the canvas image as a PIL Image."""
        return Image.fromqimage(self.image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitRecognizerApp()
    window.show()
    sys.exit(app.exec_())