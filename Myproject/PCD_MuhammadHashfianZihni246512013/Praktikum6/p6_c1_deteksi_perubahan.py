# p6_c1_deteksi_perubahan.py — Praktik C1 lanjutan: deteksi perubahan dengan pengurangan citra
import cv2
import numpy as np
from pcd_util import baca_citra, ke_gray, tampilkan


def buat_frame_kedua(img, seed=1):
    """Simulasi frame kedua CCTV: dua objek baru + sedikit noise kamera."""
    rng = np.random.default_rng(seed)
    f2 = img.copy()
    cv2.circle(f2, (360, 220), 38, (40, 60, 220), -1)
    cv2.rectangle(f2, (40, 200), (110, 270), (230, 200, 60), -1)
    tambah_noise = lambda c: np.clip(c.astype(int) + rng.normal(0, 3, c.shape), 0, 255).astype(np.uint8)
    return tambah_noise(img), tambah_noise(f2)


if __name__ == "__main__":
    f1, f2 = buat_frame_kedua(baca_citra("citra/kopi.jpg"))

    selisih = ke_gray(cv2.absdiff(f1, f2))                    # |f1 - f2|
    _, mask = cv2.threshold(selisih, 30, 255, cv2.THRESH_BINARY)
    print(f"Area berubah: {(mask == 255).mean() * 100:.1f}% piksel")

    # bandingkan dengan subtract biasa: perubahan ke arah gelap bisa hilang
    hanya_sub = ke_gray(cv2.subtract(f1, f2))
    print("Nilai maks absdiff  :", selisih.max(), "| subtract:", hanya_sub.max())

    tampilkan([("Frame 1", f1), ("Frame 2", f2), ("|f1 - f2|", selisih), ("Threshold T = 30", mask)], kolom=4, ukuran=3.5)