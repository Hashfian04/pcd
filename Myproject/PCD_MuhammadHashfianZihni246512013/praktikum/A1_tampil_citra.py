import cv2
import matplotlib.pyplot as plt

# 1. Membaca citra dari file
img = cv2.imread("../images/go_younjung.jpg")

if img is None:
    print("Citra tidak ditemukan, cek path!")
else:
    # 2. Menampilkan citra di jendela
    cv2.imshow("Citra Asli", img)
    print(type(img))  # numpy.ndarray
    print(img.shape)  # (tinggi, lebar, 3)
    print(img.dtype)  # uint8 (0–255)
    b, g, r = img[100, 50]  # piksel y=100, x=50
    print(b, g, r)
    # 3. Menunggu tombol ditekan
    cv2.waitKey(0)


    # 4. Menutup semua jendela
    cv2.destroyAllWindows()





rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(rgb); plt.show()
