import cv2
import numpy as np

# Create a black image (500x500 pixels)
img = np.zeros((500, 500, 3), dtype=np.uint8)

# Draw a red circle at the center
cv2.circle(img, (250, 250), 100, (0, 0, 255), -1)

# Display the image
cv2.imshow("OpenCV Test - Red Circle", img)

# Wait for any key press
cv2.waitKey(0)

# Close the window
cv2.destroyAllWindows()
