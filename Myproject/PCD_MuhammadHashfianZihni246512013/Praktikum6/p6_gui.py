# p6_gui.py — GUI PyQt6 untuk Praktikum 6 (menu Aritmatika dan Boolean)
import sys
import cv2
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QSlider,
                             QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox)
from p4_gui import ke_qpixmap  # dipakai ulang dari Praktikum 4
from p6_c1_aritmatika import samakan_ukuran


class JendelaP6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Praktikum 6 — Operasi Aritmatika dan Boolean")
        self.img1 = self.img2 = self.hasil = None

        self.labels = [QLabel(t) for t in ("Citra 1", "Citra 2", "Hasil")]
        baris = QHBoxLayout()
        for lbl in self.labels:
            lbl.setFixedSize(360, 300)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("border: 1px solid gray;")
            baris.addWidget(lbl)

        # slider alpha untuk blending
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100);
        self.slider.setValue(50)
        self.label_alpha = QLabel("α = 0.50 (blending)")
        self.slider.valueChanged.connect(self.blending)
        baris_slider = QHBoxLayout();
        baris_slider.addWidget(self.label_alpha);
        baris_slider.addWidget(self.slider)

        utama = QVBoxLayout();
        utama.addLayout(baris);
        utama.addLayout(baris_slider)
        wadah = QWidget();
        wadah.setLayout(utama);
        self.setCentralWidget(wadah)

        menu_file = self.menuBar().addMenu("File")
        self.aksi(menu_file, "Buka citra 1", lambda: self.buka(1))
        self.aksi(menu_file, "Buka citra 2", lambda: self.buka(2))

        menu_ar = self.menuBar().addMenu("Aritmatika")
        self.aksi(menu_ar, "Tambah (cv2.add)", lambda: self.hitung(cv2.add))
        self.aksi(menu_ar, "Tambah (operator NumPy +)", lambda: self.hitung(lambda a, b: a + b))
        self.aksi(menu_ar, "Kurang (cv2.subtract)", lambda: self.hitung(cv2.subtract))
        self.aksi(menu_ar, "Selisih mutlak (cv2.absdiff)", lambda: self.hitung(cv2.absdiff))
        self.aksi(menu_ar, "Kali (cv2.multiply)", lambda: self.hitung(lambda a, b: cv2.multiply(a, b, scale=1 / 255)))
        self.aksi(menu_ar, "Bagi (cv2.divide)",
                  lambda: self.hitung(lambda a, b: cv2.divide(a, cv2.add(b, 1), scale=128)))

        menu_bo = self.menuBar().addMenu("Boolean")
        self.aksi(menu_bo, "AND", lambda: self.hitung(cv2.bitwise_and))
        self.aksi(menu_bo, "OR", lambda: self.hitung(cv2.bitwise_or))
        self.aksi(menu_bo, "XOR", lambda: self.hitung(cv2.bitwise_xor))
        self.aksi(menu_bo, "NOT citra 1", lambda: self.hitung(lambda a, b: cv2.bitwise_not(a)))
        self.aksi(menu_bo, "Masking (mask = threshold citra 2)", self.masking)
        # Tugas Individu: Tambahan Masking Elips di tengah citra 1
        self.aksi(menu_bo, "Masking Elips (Citra 1)", self.masking_elips)

    def aksi(self, menu, teks, slot):
        a = QAction(teks, self);
        a.triggered.connect(slot);
        menu.addAction(a)

    def tampil(self, img, i):
        self.labels[i].setPixmap(ke_qpixmap(img).scaled(self.labels[i].size(), Qt.AspectRatioMode.KeepAspectRatio))

    def set_citra(self, n, img):
        if n == 1:
            self.img1 = img
            if self.img2 is not None:
                self.img2 = samakan_ukuran(img, self.img2)
        else:
            self.img2 = img if self.img1 is None else samakan_ukuran(self.img1, img)
        for i, c in enumerate((self.img1, self.img2)):
            if c is not None:
                self.tampil(c, i)

    def buka(self, n):
        path, _ = QFileDialog.getOpenFileName(self, f"Pilih citra {n}", "citra", "Citra (*.png *.jpg *.bmp)")
        if path:
            self.set_citra(n, cv2.imread(path))

    def siap(self):
        if self.img1 is None or self.img2 is None:
            QMessageBox.warning(self, "Peringatan", "Buka citra 1 dan citra 2 terlebih dahulu.")
            return False
        return True

    def hitung(self, operasi):
        if not self.siap():
            return
        self.hasil = operasi(self.img1, self.img2)
        self.tampil(self.hasil, 2)
        p1, p2, ph = self.img1[100, 100], self.img2[100, 100], self.hasil[100, 100]
        self.statusBar().showMessage(f"Piksel (x=100, y=100): citra1={p1}  citra2={p2}  hasil={ph}")

    def blending(self, nilai):
        alpha = nilai / 100
        self.label_alpha.setText(f"α = {alpha:.2f} (blending)")
        if self.img1 is not None and self.img2 is not None:
            self.hitung(lambda a, b: cv2.addWeighted(a, alpha, b, 1 - alpha, 0))

    def masking(self):
        if not self.siap():
            return
        gray2 = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)
        self.hitung(lambda a, b: cv2.bitwise_and(a, a, mask=mask))

    def masking_elips(self):
        if self.img1 is None:
            QMessageBox.warning(self, "Peringatan", "Buka citra 1 terlebih dahulu.")
            return
        h, w = self.img1.shape[:2]
        mask = np.zeros((h, w), np.uint8)
        cv2.ellipse(mask, (w // 2, h // 2), (w // 3, h // 3), 0, 0, 360, 255, -1)
        self.hasil = cv2.bitwise_and(self.img1, self.img1, mask=mask)
        self.tampil(self.hasil, 2)
        self.statusBar().showMessage("Masking Elips berhasil diterapkan pada Citra 1.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    jendela = JendelaP6()
    jendela.show()
    sys.exit(app.exec())