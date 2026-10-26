# pcd_util.py — Utility helper untuk Pengolahan Citra Digital (PCD)
import cv2
import matplotlib.pyplot as plt
import numpy as np


def baca_citra(path_berkas):
    """Membaca citra dari jalur berkas dan mengembalikan citra BGR OpenCV."""
    img = cv2.imread(path_berkas)
    if img is None:
        raise FileNotFoundError(f"Berkas citra tidak ditemukan di jalur: {path_berkas}")
    return img


def ke_gray(img):
    """Mengubah citra BGR ke Grayscale jika citra bernilai berwarna."""
    if len(img.shape) == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def ke_rgb(img):
    """Mengubah citra BGR ke RGB untuk keperluan visualisasi Matplotlib."""
    if len(img.shape) == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def tampilkan(daftar_citra, kolom=4, ukuran=3.5):
    """
    Menampilkan daftar citra menggunakan Matplotlib dalam format grid.

    daftar_citra: list of tuple (judul, img)
    kolom: jumlah kolom visualisasi
    ukuran: ukuran skala tiap subplot
    """
    n = len(daftar_citra)
    baris = (n + kolom - 1) // kolom
    fig, axes = plt.subplots(baris, kolom, figsize=(kolom * ukuran, baris * ukuran))

    # Ratakan array axes agar mudah diiterasi
    if n == 1:
        axes = np.array([axes])
    axes = np.array(axes).reshape(-1)

    for i, item in enumerate(daftar_citra):
        if len(item) == 2:
            judul, img = item
            cmap = None
        else:
            judul, img, cmap = item

        ax = axes[i]

        # Cek kanal warna
        if len(img.shape) == 2:
            ax.imshow(img, cmap=cmap if cmap else 'gray', vmin=0, vmax=255)
        else:
            ax.imshow(ke_rgb(img))

        ax.set_title(judul)
        ax.axis('off')

    # Sembunyikan subplot sisa yang tidak terpakai
    for i in range(n, len(axes)):
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()