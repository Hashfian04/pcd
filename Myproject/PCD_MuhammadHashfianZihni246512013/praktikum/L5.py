import cv2
import matplotlib.pyplot as plt

img = cv2.imread("../images/go_younjung.jpg", cv2.IMREAD_COLOR)

blue = img[:, :, 0]
green = img[:, :, 1]
red = img[:, :, 2]

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(img_rgb)
plt.title("Citra Asli")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(blue, cmap="gray")
plt.title("Kanal Blue (B)")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(green, cmap="gray")
plt.title("Kanal Green (G)")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(red, cmap="gray")
plt.title("Kanal Red (R)")
plt.axis("off")

plt.tight_layout()
plt.show()