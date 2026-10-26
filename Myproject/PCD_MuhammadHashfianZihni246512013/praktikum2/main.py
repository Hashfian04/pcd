import sys
import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QSlider, QHBoxLayout, QVBoxLayout,
                             QFileDialog, QMessageBox)
import operasi as op
from tampilan import ke_pixmap


class Jendela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Praktikum PCD')
        self.resize(1100, 650)
        self.img = None  # citra asli (BGR) — tidak pernah ditimpa
        self.gray = None  # grayscale asli — dasar semua operasi titik
        self.hasil = None  # citra hasil terakhir

        # --- dua area tampilan berdampingan ---
        self.lbl_asli = QLabel('Citra asli')
        self.lbl_hasil = QLabel('Citra hasil')
        for lbl in (self.lbl_asli, self.lbl_hasil):
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setMinimumSize(500, 450)
            lbl.setStyleSheet('border: 1px solid gray;')

        self.lbl_info = QLabel('Belum ada citra')

        # --- slider brightness (A4) ---
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(-100, 100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.ubah_brightness)
        self.lbl_b = QLabel('b = 0')

        baris_citra = QHBoxLayout()
        baris_citra.addWidget(self.lbl_asli)
        baris_citra.addWidget(self.lbl_hasil)

        baris_slider = QHBoxLayout()
        baris_slider.addWidget(QLabel('Brightness'))
        baris_slider.addWidget(self.slider)
        baris_slider.addWidget(self.lbl_b)

        tata = QVBoxLayout()
        tata.addLayout(baris_citra)
        tata.addLayout(baris_slider)
        tata.addWidget(self.lbl_info)

        pusat = QWidget()
        pusat.setLayout(tata)
        self.setCentralWidget(pusat)  # QMainWindow memakai central widget

        self.buat_menu()

    # ---------- menu ----------
    def buat_menu(self):
        menu = self.menuBar()

        m_berkas = menu.addMenu('&Berkas')
        self.tambah_aksi(m_berkas, 'Buka Citra...', self.buka_citra)
        self.tambah_aksi(m_berkas, 'Simpan Hasil...', self.simpan_hasil)

        m_warna = menu.addMenu('&Warna')
        self.tambah_aksi(m_warna, 'Grayscale rata-rata',
                         lambda: self.proses_warna(op.gray_rata2, 'rata-rata'))
        self.tambah_aksi(m_warna, 'Grayscale luminance',
                         lambda: self.proses_warna(op.gray_luminance, 'luminance'))
        self.tambah_aksi(m_warna, 'Grayscale cv2.cvtColor',
                         lambda: self.proses_warna(op.gray_opencv, 'cvtColor'))

        m_titik = menu.addMenu('&Operasi Titik')
        self.tambah_aksi(m_titik, 'Contrast a = 1,5',
                         lambda: self.proses_titik(lambda g: op.contrast(g, 1.5),
                                                   'contrast a=1,5'))
        self.tambah_aksi(m_titik, 'Contrast Stretching',
                         lambda: self.proses_titik(op.stretching, 'stretching'))
        self.tambah_aksi(m_titik, 'Negative',
                         lambda: self.proses_titik(op.negative, 'negative'))

    def tambah_aksi(self, menu, teks, fungsi):
        aksi = QAction(teks, self)
        aksi.triggered.connect(fungsi)
        menu.addAction(aksi)

    # ---------- berkas ----------
    def buka_citra(self):
        jalur, _ = QFileDialog.getOpenFileName(
            self, 'Buka Citra', '', 'Gambar (*.png *.jpg *.jpeg *.bmp)')
        if not jalur:  # pengguna menekan Batal
            return
        img = cv2.imread(jalur)
        if img is None:  # berkas rusak / bukan citra
            QMessageBox.warning(self, 'Gagal', 'Berkas tidak dapat dibaca.')
            return
        self.muat(img)

    def muat(self, img):
        self.img = img
        self.gray = op.gray_opencv(img)
        self.hasil = None
        self.lbl_asli.setPixmap(self.skala(ke_pixmap(img)))
        self.lbl_hasil.clear()
        self.slider.setValue(0)
        h, w, k = img.shape
        self.lbl_info.setText(f'Ukuran: {w} x {h} piksel  ·  kanal: {k}')

    def simpan_hasil(self):
        if self.hasil is None:
            return
        jalur, _ = QFileDialog.getSaveFileName(
            self, 'Simpan Hasil', 'hasil.png', 'PNG (*.png)')
        if jalur:
            cv2.imwrite(jalur, self.hasil)

    # ---------- pengolahan ----------
    def proses_warna(self, fungsi, nama):
        if self.img is None:
            return
        self.tampilkan_hasil(fungsi(self.img), f'grayscale {nama}')

    def proses_titik(self, fungsi, nama):
        if self.gray is None:
            return
        self.tampilkan_hasil(fungsi(self.gray), nama)

    def ubah_brightness(self, nilai):
        self.lbl_b.setText(f'b = {nilai}')
        if self.gray is None:
            return
        # selalu dari self.gray asli, agar efek tidak menumpuk
        self.tampilkan_hasil(op.brightness(self.gray, nilai), f'brightness b={nilai}')

    def tampilkan_hasil(self, citra, nama):
        self.hasil = citra
        self.lbl_hasil.setPixmap(self.skala(ke_pixmap(citra)))
        self.lbl_info.setText(
            f'Operasi: {nama}  ·  min={citra.min()}  max={citra.max()}  '
            f'rata-rata={citra.mean():.1f}')

    def skala(self, pixmap):
        return pixmap.scaled(500, 450, Qt.AspectRatioMode.KeepAspectRatio,
                             Qt.TransformationMode.SmoothTransformation)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Jendela()
    w.show()
    sys.exit(app.exec())