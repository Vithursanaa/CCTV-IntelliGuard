#import libraries
import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8n
model = YOLO('yolov8n.pt')

# Open the webcam
cap = cv2.VideoCapture(0)

# Read the first frame to initialize motion detection
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

# Define a virtual line (y-coordinate) for direction detection
# Adjust based on your camera position
frame_height = prev_frame.shape[0]
line_y = frame_height // 2

# Store previous positions of people
previous_centers = {}

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
        if cv2.contourArea(contour) > 1000:
            motion_detected = True
            break

    if motion_detected:
        results = model(frame, verbose=False)

        current_centers = {}

        for r in results:
            for box_id, box in enumerate(r.boxes):
                cls = int(box.cls[0])
                label = model.names[cls]
                if label == 'person':
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx = int((x1 + x2) / 2)  # center X
                    cy = int((y1 + y2) / 2)  # center Y

                    # Draw bounding box & center point
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)

                    # Store current center
                    current_centers[box_id] = (cx, cy)

                    # Direction detection
                    if box_id in previous_centers:
                        prev_cx, prev_cy = previous_centers[box_id]

                        # If previously above the line and now below → entering
                        if prev_cy < line_y and cy >= line_y:
                            cv2.putText(frame, "Entering", (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                            print("🚶‍♂️ Entering the room")
                        # If previously below the line and now above → leaving
                        elif prev_cy > line_y and cy <= line_y:
                            cv2.putText(frame, "Leaving", (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                            print("🚶‍♂️ Leaving the room")

        # Update previous centers
        previous_centers = current_centers

    # Draw the virtual line
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0,255,255), 2)

    # Show result
    cv2.imshow("Motion + YOLO + Direction Detection", frame)

    prev_gray = gray.copy()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
