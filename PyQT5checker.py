# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 17:04:08 2025

@author: varsha
"""

from PyQt5.QtGui import QImage
from PIL import Image

# Create a dummy QImage
qimage = QImage(100, 100, QImage.Format_RGB32)
qimage.fill(0)  # Fill with black

# Convert QImage to Pillow Image
try:
    pil_image = Image.fromqimage(qimage)
    print("Conversion successful:", isinstance(pil_image, Image.Image))
except ImportError as e:
    print("Error:", e)