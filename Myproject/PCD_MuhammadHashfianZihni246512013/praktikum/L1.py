import cv2

img1 = cv2.imread("../images/motor1.jpg")
img2 = cv2.imread("../images/motor2.jpg")
img3 = cv2.imread("../images/motor3.jpg")

cv2.imshow("Citra Pertama", img1)
cv2.imshow("Citra Kedua", img2)
cv2.imshow("Citra Ketiga", img3)

cv2.waitKey(0)
cv2.destroyAllWindows()
