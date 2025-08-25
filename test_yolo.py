#import libraries
import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8n 
model = YOLO('yolov8n.pt')

# Notice the quotes "" and the %40 for @ in the password
url = "rtsp://student1:Stu1%40cse@10.8.104.13:554/Streaming/Channels/101"
cap = cv2.VideoCapture(url)

# Read the first frame to initialize motion detection
ret, prev_frame = cap.read()

#Converts the first video frame (captured from the webcam) from color (BGR) to grayscale format.
#cv2.cvtColor(....) - OpenCV function used to convert the color space of an image
#prev_frame - original color image (from webcam), in BGR format by default
#cv2.COLOR_BGR2GRAY- flag tells OpenCV to convert from BGR to Grayscale (shades of gray, no color)
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

#Blurs the prev_gray image using a Gaussian filter
#cv2.GaussianBlur(src, ksize, sigmaX) - src/input image, ksize/kernal size- size of the filter window, sigmaX/Standard deviation in X direction 
#(21, 21) is a common choice for motion detection to ensure enough smoothing.
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0) 

#Reads a new frame from the webcam in each loop iteration, if no frame is read (e.g., camera error), the loop stops.
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert current frame to grayscale and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Compute difference between previous and current frame
    diff = cv2.absdiff(prev_gray, gray)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find motion contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Sensitivity
            motion_detected = True
            break

    if motion_detected:
        print("📸 Motion detected... Checking with YOLO.")
        results = model(frame, verbose=False)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                if label == 'person':
                    print("👤 Human detected!")
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    # Show result
    cv2.imshow("Motion + YOLO Human Detection", frame)

    # Update previous frame
    prev_gray = gray.copy()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
