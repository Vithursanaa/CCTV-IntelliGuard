import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque
import time
import os

# ------------------------------
# CONFIGURATION
# ------------------------------
# YOLO model: choose 'yolov8n.pt', 'yolov8s.pt', or 'yolov8m.pt'
model = YOLO('yolov8s.pt')

# RTSP stream URL
url = "rtsp://student1:Stu1%40cse@10.8.104.13:554/Streaming/Channels/102"

# Open RTSP stream with FFMPEG
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

# Background subtractor for motion detection
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=True)

# Frame buffer for pre-event recording (5 seconds @ 25 fps → 125 frames)
frame_buffer = deque(maxlen=125)

# Recording state
recording = False
record_frames = []
cooldown = 250  # record 250 extra frames after motion stops (~10 sec @25fps)
frames_after_motion = 0

# Directory to save videos
SAVE_DIR = "recorded_events_02"
os.makedirs(SAVE_DIR, exist_ok=True)

# ------------------------------
# FUNCTIONS
# ------------------------------
def motion_detected(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
    # noise reduction
    fgmask = cv2.erode(fgmask, None, iterations=2)
    fgmask = cv2.dilate(fgmask, None, iterations=2)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return any(cv2.contourArea(c) > 500 for c in contours)

def save_video(frames, filename="event.avi", fps=25):
    if not frames:
        return None
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    for f in frames:
        out.write(f)
    out.release()
    print(f"[INFO] Saved video: {filename}")
    return filename

# ------------------------------
# MAIN LOOP
# ------------------------------
if not cap.isOpened():
    print("[ERROR] Cannot open RTSP stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("[WARN] Frame not received, retrying...")
        time.sleep(0.5)
        continue

    # store in circular buffer
    frame_buffer.append(frame.copy())

    # Step 1: motion detection
    motion = motion_detected(frame)

    # Step 2: YOLO detection (only if motion detected, to save resources)
    human_detected = False
    if motion:
        results = model(frame, verbose=False)
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if model.names[cls] == "person":
                    human_detected = True
                    break

    # Step 3: recording logic
    if human_detected:
        if not recording:
            recording = True
            record_frames = list(frame_buffer)  # start with pre-event frames
            print("[INFO] Started recording event")
        record_frames.append(frame.copy())
        frames_after_motion = cooldown
    elif recording:
        if frames_after_motion > 0:
            record_frames.append(frame.copy())
            frames_after_motion -= 1
        else:
            timestamp = int(time.time())
            filename = os.path.join(SAVE_DIR, f"event_{timestamp}.avi")
            save_video(record_frames, filename)
            recording = False
            record_frames = []

    # Optional: show preview
    cv2.imshow("CCTV Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

