"""operasi.py - fungsi pengolahan citra tanpa GUI."""
import cv2
import numpy as np


# ---------- Grayscale ----------
def gray_rata2(img):
    """Grayscale menggunakan rata-rata kanal BGR."""
    return img.astype(np.float32).mean(axis=2).astype(np.uint8)


def gray_luminance(img):
    """Grayscale berdasarkan luminance ITU-R BT.601."""
    b = img[:, :, 0].astype(np.float32)
    g = img[:, :, 1].astype(np.float32)
    r = img[:, :, 2].astype(np.float32)
    return (0.114 * b + 0.587 * g + 0.299 * r).astype(np.uint8)


def gray_opencv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# ---------- Operasi titik ----------
def brightness(gray, b):
    return np.clip(gray.astype(np.int16) + b, 0, 255).astype(np.uint8)


def contrast(gray, a):
    return np.clip(gray.astype(np.float32) * a, 0, 255).astype(np.uint8)


def stretching(gray):
    rmin, rmax = int(gray.min()), int(gray.max())
    if rmin == rmax:
        return gray.copy()
    hasil = (gray.astype(np.float32) - rmin) / (rmax - rmin) * 255
    return np.clip(hasil, 0, 255).astype(np.uint8)


def negative(gray):
    return 255 - gray


# ---------- Operasi geometri ----------
def translasi(img, tx, ty):
    h, w = img.shape[:2]
    matriks = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(img, matriks, (w, h))


def rotasi(img, sudut):
    """Rotasi dengan kanvas penuh; sudut positif berlawanan arah jarum jam."""
    sudut_mod = sudut % 360
    rotasi_90 = {
        90: cv2.ROTATE_90_COUNTERCLOCKWISE,
        180: cv2.ROTATE_180,
        270: cv2.ROTATE_90_CLOCKWISE,
    }
    if sudut_mod == 0:
        return img.copy()
    if sudut_mod in rotasi_90:
        return cv2.rotate(img, rotasi_90[sudut_mod])

    h, w = img.shape[:2]
    pusat = (w / 2, h / 2)
    matriks = cv2.getRotationMatrix2D(pusat, sudut, 1.0)
    cosinus, sinus = abs(matriks[0, 0]), abs(matriks[0, 1])
    lebar_baru = int(h * sinus + w * cosinus)
    tinggi_baru = int(h * cosinus + w * sinus)
    matriks[0, 2] += lebar_baru / 2 - pusat[0]
    matriks[1, 2] += tinggi_baru / 2 - pusat[1]
    return cv2.warpAffine(img, matriks, (lebar_baru, tinggi_baru))


def flip(img, kode):
    """kode: 1 horizontal, 0 vertikal, -1 horizontal dan vertikal."""
    return cv2.flip(img, kode)


def skala(img, faktor, interpolasi=cv2.INTER_LINEAR):
    if faktor <= 0:
        raise ValueError("Faktor skala harus lebih besar dari 0.")
    return cv2.resize(img, None, fx=faktor, fy=faktor, interpolation=interpolasi)


def crop(img, x1, y1, x2, y2):
    """Crop menggunakan koordinat (x1, y1) sampai (x2, y2), batas akhir eksklusif."""
    h, w = img.shape[:2]
    x1, x2 = max(0, min(w, x1)), max(0, min(w, x2))
    y1, y2 = max(0, min(h, y1)), max(0, min(h, y2))
    if x2 <= x1 or y2 <= y1:
        return img[0:0, 0:0].copy()
    return img[y1:y2, x1:x2].copy()
