import cv2

img = cv2.imread("../images/go_younjung.jpg")

cv2.imshow("Citra Otomatis", img)

cv2.waitKey(3000)
cv2.destroyAllWindows()
