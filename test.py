import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8n model
model = YOLO('yolov8n.pt')

# RTSP URL
url = "rtsp://student1:Stu1%40cse@10.8.104.13:554/Streaming/Channels/102"

# OpenCV VideoCapture (default backend)
cap = cv2.VideoCapture(url)

# Read first frame to initialize motion detection
while True:
    ret, prev_frame = cap.read()
    if ret and prev_frame is not None:
        break
    print("⚠️ Waiting for a valid first frame...")

# Convert to grayscale and blur
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("⚠️ Skipping bad frame")
        continue

    # Convert current frame to grayscale and blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Compute difference between previous and current frame
    diff = cv2.absdiff(prev_gray, gray)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find motion contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion_detected = any(cv2.contourArea(c) > 1000 for c in contours)  # adjust sensitivity

    if motion_detected:
        print("📸 Motion detected... Checking with YOLO for humans.")
        # Optionally resize frame for faster YOLO detection
        frame_resized = cv2.resize(frame, (640, 640))
        results = model(frame_resized, verbose=False)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]
                if label == 'person':
                    print("👤 Human detected!")
                    # Map coordinates back to original frame size
                    x_scale = frame.shape[1] / 640
                    y_scale = frame.shape[0] / 640
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    x1, y1, x2, y2 = int(x1 * x_scale), int(y1 * y_scale), int(x2 * x_scale), int(y2 * y_scale)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Motion + YOLO Human Detection", frame)

    # Update previous frame
    prev_gray = gray.copy()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
