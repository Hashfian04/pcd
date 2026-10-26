"""main.py - aplikasi praktikum PCD: grayscale, operasi titik, dan geometri."""
import sys
import cv2

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QSlider,
    QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QInputDialog
)

import operasi as op
from tampilan import ke_pixmap


class Jendela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Praktikum PCD - Operasi Geometri")
        self.resize(1150, 720)

        self.img = None       # Citra asli berwarna (BGR), tidak ditimpa operasi.
        self.gray = None      # Grayscale dasar untuk operasi titik.
        self.hasil = None     # Hasil operasi terakhir.

        self.lbl_asli = QLabel("Citra asli\nBuka gambar melalui menu Berkas")
        self.lbl_hasil = QLabel("Citra hasil")
        for label in (self.lbl_asli, self.lbl_hasil):
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setMinimumSize(500, 450)
            label.setStyleSheet("border: 1px solid #888; background: #f5f5f5;")

        self.lbl_info = QLabel("Belum ada citra.")
        self.lbl_info.setWordWrap(True)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(-100, 100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.ubah_brightness)
        self.lbl_b = QLabel("b = 0")

        baris_citra = QHBoxLayout()
        baris_citra.addWidget(self.lbl_asli)
        baris_citra.addWidget(self.lbl_hasil)

        baris_slider = QHBoxLayout()
        baris_slider.addWidget(QLabel("Brightness"))
        baris_slider.addWidget(self.slider)
        baris_slider.addWidget(self.lbl_b)

        tata = QVBoxLayout()
        tata.addLayout(baris_citra)
        tata.addLayout(baris_slider)
        tata.addWidget(self.lbl_info)

        pusat = QWidget()
        pusat.setLayout(tata)
        self.setCentralWidget(pusat)
        self.buat_menu()

    # ---------- Menu ----------
    def buat_menu(self):
        menu = self.menuBar()

        m_berkas = menu.addMenu("&Berkas")
        self.tambah_aksi(m_berkas, "Buka Citra...", self.buka_citra)
        self.tambah_aksi(m_berkas, "Simpan Hasil...", self.simpan_hasil)

        m_warna = menu.addMenu("&Warna")
        self.tambah_aksi(
            m_warna, "Grayscale rata-rata",
            lambda: self.proses_warna(op.gray_rata2, "rata-rata")
        )
        self.tambah_aksi(
            m_warna, "Grayscale luminance",
            lambda: self.proses_warna(op.gray_luminance, "luminance")
        )
        self.tambah_aksi(
            m_warna, "Grayscale OpenCV",
            lambda: self.proses_warna(op.gray_opencv, "OpenCV")
        )

        m_titik = menu.addMenu("&Operasi Titik")
        self.tambah_aksi(
            m_titik, "Contrast (a = 1,5)",
            lambda: self.proses_titik(
                lambda gray: op.contrast(gray, 1.5), "contrast a=1,5"
            )
        )
        self.tambah_aksi(
            m_titik, "Contrast Stretching",
            lambda: self.proses_titik(op.stretching, "contrast stretching")
        )
        self.tambah_aksi(
            m_titik, "Negative",
            lambda: self.proses_titik(op.negative, "negative")
        )

        m_geo = menu.addMenu("&Geometri")
        self.tambah_aksi(m_geo, "Translasi...", self.translasi)
        self.tambah_aksi(m_geo, "Rotasi...", self.rotasi)
        self.tambah_aksi(m_geo, "Flip / Transpose...", self.flip)
        self.tambah_aksi(m_geo, "Penskalaan...", self.skala)
        self.tambah_aksi(m_geo, "Crop...", self.crop)

    @staticmethod
    def tambah_aksi(menu, teks, fungsi):
        aksi = QAction(teks, menu)
        aksi.triggered.connect(fungsi)
        menu.addAction(aksi)

    # ---------- Berkas ----------
    def buka_citra(self):
        # PILIH FOTO: dialog ini memungkinkan kamu memilih file dari direktori mana pun.
        # Jika ingin memuat otomatis, ganti nilai awal dialog di bawah dengan direktori foto kamu.
        jalur, _ = QFileDialog.getOpenFileName(
            self, "Buka Citra", "", "Gambar (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        if not jalur:
            return
        img = cv2.imread(jalur)
        if img is None:
            QMessageBox.warning(self, "Gagal", "Berkas gambar tidak dapat dibaca.")
            return
        self.muat(img)

    def muat(self, img):
        self.img = img.copy()
        self.gray = op.gray_opencv(self.img)
        self.hasil = None
        self.lbl_asli.setPixmap(self.skala_tampil(ke_pixmap(self.img)))
        self.lbl_hasil.setText("Citra hasil")
        self.slider.blockSignals(True)
        self.slider.setValue(0)
        self.slider.blockSignals(False)
        self.lbl_b.setText("b = 0")
        tinggi, lebar = self.img.shape[:2]
        kanal = 1 if self.img.ndim == 2 else self.img.shape[2]
        self.lbl_info.setText(
            f"Citra asli dimuat: {lebar} x {tinggi} piksel · kanal: {kanal}"
        )

    def simpan_hasil(self):
        if self.hasil is None:
            QMessageBox.information(self, "Info", "Belum ada hasil untuk disimpan.")
            return
        jalur, _ = QFileDialog.getSaveFileName(
            self, "Simpan Hasil", "hasil.png",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)"
        )
        if jalur:
            berhasil = cv2.imwrite(jalur, self.hasil)
            if not berhasil:
                QMessageBox.warning(self, "Gagal", "Hasil tidak dapat disimpan.")

    # ---------- Operasi warna dan titik ----------
    def proses_warna(self, fungsi, nama):
        if self.img is None:
            self.peringatan_belum_ada_citra()
            return
        self.tampilkan_hasil(fungsi(self.img), f"grayscale {nama}")

    def proses_titik(self, fungsi, nama):
        if self.gray is None:
            self.peringatan_belum_ada_citra()
            return
        self.tampilkan_hasil(fungsi(self.gray), nama)

    def ubah_brightness(self, nilai):
        self.lbl_b.setText(f"b = {nilai}")
        if self.gray is not None:
            self.tampilkan_hasil(op.brightness(self.gray, nilai), f"brightness b={nilai}")

    # ---------- Operasi geometri: selalu dari self.img asli ----------
    def translasi(self):
        if self.img is None:
            self.peringatan_belum_ada_citra()
            return
        tx, ok = QInputDialog.getInt(self, "Translasi", "tx (piksel, + ke kanan):", 80, -2000, 2000)
        if not ok:
            return
        ty, ok = QInputDialog.getInt(self, "Translasi", "ty (piksel, + ke bawah):", 40, -2000, 2000)
        if ok:
            self.tampilkan_hasil(op.translasi(self.img, tx, ty), f"translasi tx={tx}, ty={ty}")

    def rotasi(self):
        if self.img is None:
            self.peringatan_belum_ada_citra()
            return
        sudut, ok = QInputDialog.getInt(
            self, "Rotasi", "Sudut (derajat; positif = berlawanan jarum jam):",
            30, -360, 360
        )
        if ok:
            self.tampilkan_hasil(op.rotasi(self.img, sudut), f"rotasi {sudut}°")

    def flip(self):
        if self.img is None:
            self.peringatan_belum_ada_citra()
            return
        pilihan = ["Horizontal", "Vertikal", "Keduanya", "Transpose"]
        jenis, ok = QInputDialog.getItem(self, "Flip / Transpose", "Jenis operasi:", pilihan, 0, False)
        if not ok:
            return
        if jenis == "Transpose":
            hasil = cv2.transpose(self.img)
        else:
            kode = {"Horizontal": 1, "Vertikal": 0, "Keduanya": -1}[jenis]
            hasil = op.flip(self.img, kode)
        self.tampilkan_hasil(hasil, jenis.lower() if jenis == "Transpose" else f"flip {jenis.lower()}")

    def skala(self):
        if self.img is None:
            self.peringatan_belum_ada_citra()
            return
        faktor, ok = QInputDialog.getDouble(
            self, "Penskalaan", "Faktor skala:", 2.0, 0.1, 8.0, 2
        )
        if not ok:
            return
        daftar = {
            "Linear": cv2.INTER_LINEAR,
            "Nearest": cv2.INTER_NEAREST,
            "Cubic": cv2.INTER_CUBIC,
            "Area": cv2.INTER_AREA,
        }
        nama, ok = QInputDialog.getItem(
            self, "Penskalaan", "Metode interpolasi:", list(daftar), 0, False
        )
        if ok:
            hasil = op.skala(self.img, faktor, daftar[nama])
            self.tampilkan_hasil(hasil, f"skala {faktor}x ({nama.lower()})")

    def crop(self):
        if self.img is None:
            self.peringatan_belum_ada_citra()
            return
        teks, ok = QInputDialog.getText(
            self, "Crop", "Koordinat x1, y1, x2, y2:",
            text="160, 60, 360, 260"  # NILAI DUMMY: ubah koordinat sesuai gambar kamu.
        )
        if not ok:
            return
        try:
            bagian = [int(v.strip()) for v in teks.split(",")]
            if len(bagian) != 4:
                raise ValueError
            x1, y1, x2, y2 = bagian
        except ValueError:
            QMessageBox.warning(self, "Crop", "Masukkan empat bilangan bulat: x1, y1, x2, y2.")
            return
        hasil = op.crop(self.img, x1, y1, x2, y2)
        if hasil.size == 0:
            QMessageBox.warning(self, "Crop", "Area crop kosong atau koordinat tidak valid.")
            return
        self.tampilkan_hasil(hasil, f"crop ({x1},{y1})-({x2},{y2})")

    # ---------- Tampilan ----------
    def tampilkan_hasil(self, citra, nama):
        self.hasil = citra.copy()
        self.lbl_hasil.setPixmap(self.skala_tampil(ke_pixmap(self.hasil)))
        tinggi, lebar = citra.shape[:2]
        self.lbl_info.setText(
            f"Operasi: {nama} · ukuran hasil: {lebar} x {tinggi} piksel · "
            f"min={int(citra.min())} · max={int(citra.max())}"
        )

    @staticmethod
    def skala_tampil(pixmap):
        return pixmap.scaled(
            520, 470,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def peringatan_belum_ada_citra(self):
        QMessageBox.information(self, "Info", "Silakan buka citra terlebih dahulu melalui menu Berkas.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    jendela = Jendela()
    jendela.show()
    sys.exit(app.exec())
