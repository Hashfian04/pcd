# p4_gui.py — Helper GUI PyQt6 dan Konversi Citra PCD
import sys
import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


def ke_qpixmap(img):
    """
    Mengubah citra OpenCV/NumPy (BGR, Grayscale, atau Biner)
    menjadi QPixmap agar dapat ditampilkan pada QLabel PyQt6.
    """
    if img is None:
        return QPixmap()

    # Cek jika citra adalah Grayscale / Biner (2 dimensi)
    if len(img.shape) == 2:
        h, w = img.shape
        # Format QImage.Format.Format_Grayscale8 untuk citra 8-bit 1 kanal
        q_img = QImage(img.data, w, h, w, QImage.Format.Format_Grayscale8)

    # Cek jika citra adalah Berwarna BGR (3 dimensi)
    elif len(img.shape) == 3 and img.shape[2] == 3:
        h, w, ch = img.shape
        bytes_per_line = ch * w
        # Ubah BGR standar OpenCV ke RGB untuk PyQt6
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

    else:
        return QPixmap()

    return QPixmap.fromImage(q_img)


# Kelas jendela dasar Praktikum 4 (opsional jika ingin dijalankan mandiri)
class JendelaP4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Praktikum 4 — Preview Citra")
        self.label_citra = QLabel("Belum ada citra")
        self.label_citra.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label_citra)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def tampilkan_citra(self, img):
        pixmap = ke_qpixmap(img)
        if not pixmap.isNull():
            self.label_citra.setPixmap(pixmap.scaled(
                self.label_citra.size(),
                Qt.AspectRatioMode.KeepAspectRatio
            ))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    jendela = JendelaP4()
    jendela.resize(400, 300)
    jendela.show()
    sys.exit(app.exec())