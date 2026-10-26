"""tampilan.py - konversi citra NumPy menjadi QPixmap."""
import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap


def ke_pixmap(citra):
    """Mendukung citra grayscale (2D) dan citra berwarna BGR (3D)."""
    if citra.ndim == 2:
        array = np.ascontiguousarray(citra)
        tinggi, lebar = array.shape
        qimg = QImage(
            array.data, lebar, tinggi, lebar,
            QImage.Format.Format_Grayscale8
        )
    else:
        rgb = np.ascontiguousarray(cv2.cvtColor(citra, cv2.COLOR_BGR2RGB))
        tinggi, lebar, _ = rgb.shape
        qimg = QImage(
            rgb.data, lebar, tinggi, 3 * lebar,
            QImage.Format.Format_RGB888
        )
    # copy() memastikan QImage memiliki salinan data sendiri.
    return QPixmap.fromImage(qimg.copy())
