import cv2

img = cv2.imread('photos/sample.png')

if img is None:
    print("Failed to load image.")
else:
    cv2.imshow("Loaded Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
