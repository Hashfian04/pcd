# p6_c2_boolean.py — Praktik C2: operasi boolean (bitwise) dan masking
import cv2
import numpy as np
from pcd_util import baca_citra, tampilkan

if __name__ == "__main__":
    # 1. Operasi bit pada satu nilai piksel
    a, b = np.uint8(200), np.uint8(170)
    for nama, hasil in (("AND", a & b), ("OR", a | b), ("XOR", a ^ b), ("NOT a", ~a)):
        print(f"{nama:<6} = {int(hasil):3d} = {int(hasil):08b}")

    # 2. Dua citra biner
    A = np.zeros((300, 300), np.uint8)
    cv2.circle(A, (125, 150), 95, 255, -1)                   # lingkaran putih
    B = np.zeros((300, 300), np.uint8)
    cv2.rectangle(B, (140, 60), (270, 240), 255, -1)         # persegi putih

    dan = cv2.bitwise_and(A, B)
    atau = cv2.bitwise_or(A, B)
    xor = cv2.bitwise_xor(A, B)
    bukan = cv2.bitwise_not(A)

    # hukum De Morgan: NOT(A OR B) = (NOT A) AND (NOT B)
    kanan = cv2.bitwise_and(cv2.bitwise_not(A), cv2.bitwise_not(B))
    print("De Morgan terbukti:", np.array_equal(cv2.bitwise_not(atau), kanan))

    # 3. Masking pada citra berwarna
    img = baca_citra("citra/kucing.png")
    mask = np.zeros(img.shape[:2], np.uint8)                 # satu kanal, semua 0
    cv2.ellipse(mask, (225, 150), (170, 135), 0, 0, 360, 255, -1)
    objek = cv2.bitwise_and(img, img, mask=mask)
    latar = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask))

    tampilkan([("A", A), ("B", B), ("A AND B", dan), ("A OR B", atau), ("A XOR B", xor), ("NOT A", bukan)], kolom=6, ukuran=2.5)
    tampilkan([("Citra", img), ("Mask", mask), ("Objek", objek), ("Latar", latar)], kolom=4, ukuran=3.5)