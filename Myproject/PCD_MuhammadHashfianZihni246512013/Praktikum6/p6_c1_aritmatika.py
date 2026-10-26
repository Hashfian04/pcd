# p6_c1_aritmatika.py — Praktik C1: operasi aritmatika dua citra
import cv2
import numpy as np
from pcd_util import baca_citra, tampilkan


def samakan_ukuran(img1, img2):
    """Ubah ukuran img2 agar sama dengan img1 (cv2.resize menerima (lebar, tinggi))."""
    h, w = img1.shape[:2]
    return cv2.resize(img2, (w, h), interpolation=cv2.INTER_AREA)


if __name__ == "__main__":
    # 1. Saturasi vs wraparound pada nilai tunggal
    a = np.full((1, 1), 200, np.uint8)
    b = np.full((1, 1), 100, np.uint8)
    c = np.full((1, 1), 50, np.uint8)
    print("200 + 100 -> cv2.add :", cv2.add(a, b)[0, 0], "| NumPy :", (a + b)[0, 0])
    print(" 50 - 100 -> cv2.sub :", cv2.subtract(c, b)[0, 0], "| NumPy :", (c - b)[0, 0])

    # 2. Empat operasi pada dua citra
    img1 = baca_citra("citra/kopi.jpg")
    img2 = samakan_ukuran(img1, baca_citra("citra/kucing.jpg"))

    tambah = cv2.add(img1, img2)                              # saturasi ke 255
    kurang = cv2.subtract(img1, img2)                         # saturasi ke 0
    kali = cv2.multiply(img1, img2, scale=1 / 255)            # hasil tetap 0-255
    bagi = cv2.divide(img1, cv2.add(img2, 1), scale=128)      # +1 mencegah pembagian nol

    # 3. Operator NumPy (wraparound) vs cara yang benar
    salah = img1 + img2
    benar = np.clip(img1.astype(np.int16) + img2, 0, 255).astype(np.uint8)
    print("np.clip == cv2.add      :", np.array_equal(benar, tambah))
    print(f"Piksel berbeda (+ vs add): {(salah != tambah).mean() * 100:.1f}%")

    # 4. Blending
    campur = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)

    tampilkan([("Kucing", img1), ("Kopi", img2), ("cv2.add", tambah), ("img1 + img2 (NumPy)", salah),
               ("cv2.subtract", kurang), ("cv2.multiply", kali), ("cv2.divide", bagi),
               ("addWeighted 0,5", campur)], kolom=4, ukuran=3.5)