import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap


def ke_pixmap(citra):
    """Ubah array NumPy (grayscale atau BGR) menjadi QPixmap."""
    if citra.ndim == 2:  # grayscale
        citra = np.ascontiguousarray(citra)
        h, w = citra.shape
        qimg = QImage(citra.data, w, h, w,  # bytesPerLine = w
                      QImage.Format.Format_Grayscale8)
    else:  # berwarna
        rgb = np.ascontiguousarray(cv2.cvtColor(citra, cv2.COLOR_BGR2RGB))
        h, w, _ = rgb.shape
        qimg = QImage(rgb.data, w, h, 3 * w,  # bytesPerLine = 3w
                      QImage.Format.Format_RGB888)

    # .copy() membuat QImage memiliki datanya sendiri,
    # sehingga aman walaupun array sumber dihapus
    return QPixmap.fromImage(qimg.copy())