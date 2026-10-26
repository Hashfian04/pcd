import cv2

img = cv2.imread("../images/motor5.jpg", cv2.IMREAD_COLOR)

tinggi, lebar, kanal = img.shape

sudut = {
"Kiri atas": (0, 0),
"Kanan atas": (lebar - 1, 0),
"Kiri bawah": (0, tinggi - 1),
"Kanan bawah": (lebar - 1, tinggi - 1)
}

for nama, (x, y) in sudut.items():
    b, g, r = img[y, x]
    print(f"{nama} - Koordinat ({x}, {y}):")
    print(f"B = {b}, G = {g}, R = {r}")
    print()
