import cv2

img_color = cv2.imread("../images/motor4.jpg", cv2.IMREAD_COLOR)
img_gray = cv2.imread("../images/motor4.jpg", cv2.IMREAD_GRAYSCALE)

cv2.imshow("Citra Berwarna", img_color)
cv2.imshow("Citra Grayscale", img_gray)

print("Shape citra berwarna:", img_color.shape)
print("Shape citra grayscale:", img_gray.shape)

cv2.waitKey(0)
cv2.destroyAllWindows()
