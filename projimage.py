import cv2
image = cv2.imread("cat.jpg")
image=cv2.circle(
    image,
    (135, 90),
    50,
    (0, 200, 270),
    3
)
cv2.imshow("My Image 1", image)
cv2.waitKey(0)
cv2.destroyAllWindows()