import cv2
import matplotlib.pyplot as plt

img = cv2.imread("../images/go_younjung.jpg")
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Tanpa konversi (BGR)")

plt.subplot(1, 2, 2)
plt.imshow(rgb)
plt.title("Setelah konversi (RGB)")
plt.show()
