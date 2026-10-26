"""operasi.py — fungsi pengolahan citra (tanpa widget, bisa diuji tanpa GUI)."""
import cv2
import numpy as np


# ---------- A3: grayscale ----------
def gray_rata2(img):
    """(R + G + B) / 3 — ingat urutan OpenCV adalah B, G, R."""
    return img.astype(np.float32).mean(axis=2).astype(np.uint8)


def gray_luminance(img):
    """0,299 R + 0,587 G + 0,114 B (ITU-R BT.601)."""
    B = img[:, :, 0].astype(np.float32)
    G = img[:, :, 1].astype(np.float32)
    R = img[:, :, 2].astype(np.float32)
    return (0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)


def gray_opencv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# ---------- A4 - A7: operasi titik ----------
def brightness(gray, b):
    """A4: s = r + b, dengan clipping ke 0-255."""
    return np.clip(gray.astype(np.int16) + b, 0, 255).astype(np.uint8)


def contrast(gray, a):
    """A5: s = a x r, dengan clipping ke 0-255."""
    return np.clip(gray.astype(np.float32) * a, 0, 255).astype(np.uint8)


def stretching(gray):
    """A6: s = (r - rmin) / (rmax - rmin) x 255."""
    rmin, rmax = int(gray.min()), int(gray.max())
    if rmax == rmin:  # citra satu warna: hindari bagi nol
        return gray.copy()
    hasil = (gray.astype(np.float32) - rmin) / (rmax - rmin) * 255
    return np.clip(hasil, 0, 255).astype(np.uint8)


def negative(gray):
    """A7: s = 255 - r."""
    return 255 - gray