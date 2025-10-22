import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque
import time
import os
import requests
import subprocess

# ------------------------------
# TELEGRAM CONFIGURATION
# ------------------------------
BOT_TOKEN = "7754122601:AAGga5R6f1rd-C4zGNw2w88hS0zpg6ZpKoc"  
CHAT_ID = "1246393786"

def send_telegram_message(text, retries=3):
    """Send Telegram text message with retries and error handling"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    
    for attempt in range(1, retries + 1):
        try:
            r = requests.post(url, data=data, timeout=10)
            if r.status_code == 200:
                print("[INFO] Telegram message sent successfully.")
                return
            else:
                print(f"[WARN] Telegram returned {r.status_code}: {r.text} (attempt {attempt}/{retries})")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Telegram message failed (attempt {attempt}/{retries}): {e}")
        time.sleep(3)  # wait before retry
    
    print("[FAIL] Could not send Telegram message after retries.")


def send_telegram_video(video_path, caption="Human Detected!", retries=3):
    """Send Telegram video with compression, retries, and error handling"""
    if not os.path.exists(video_path):
        print(f"[ERROR] Video file not found: {video_path}")
        return

    # Compress if >49MB
    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    if size_mb > 49:
        compressed_path = video_path.rsplit('.', 1)[0] + "_compressed.mp4"
        print(f"[INFO] Compressing video ({size_mb:.1f} MB) → {compressed_path} ...")
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path,
            "-vcodec", "libx264", "-crf", "30",
            compressed_path
        ])
        video_path = compressed_path
        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"[INFO] Compressed video size: {size_mb:.1f} MB")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    
    for attempt in range(1, retries + 1):
        try:
            with open(video_path, "rb") as video_file:
                r = requests.post(
                    url,
                    data={"chat_id": CHAT_ID, "caption": caption},
                    files={"video": video_file},
                    timeout=60
                )
            if r.status_code == 200:
                print("[INFO] Telegram video sent successfully.")
                return
            else:
                print(f"[WARN] Telegram API returned {r.status_code}: {r.text} (attempt {attempt}/{retries})")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Telegram video failed (attempt {attempt}/{retries}): {e}")
        time.sleep(5)
    
    print("[FAIL] Could not send Telegram video after {retries} attempts.")

# ------------------------------
# CCTV CONFIGURATION
# ------------------------------
# YOLO model: choose 'yolov8n.pt', 'yolov8s.pt', or 'yolov8m.pt'
model = YOLO('yolov8s.pt')

# RTSP stream URL
url = "rtsp://student1:Stu1%40cse@10.8.104.13:554/Streaming/Channels/102?tcp"

# Open RTSP stream with FFMPEG
#cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

# FFmpeg subprocess to read raw BGR frames from RTSP
ffmpeg_cmd = [
    "ffmpeg",
    "-rtsp_transport", "tcp",
    "-i", url,
    "-vf", "scale=640:480",      # scale down
    "-c:v", "h264_mmal",         # hardware decode
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",
    "-vsync", "0",
    "-"
]
pipe = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

# Set camera resolution (replace with your camera's actual width & height)
width, height = 640, 480

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
SAVE_DIR = "recorded_events_telegram"
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
if pipe.stdout is None:
    print("[ERROR] Cannot open RTSP stream via FFmpeg")
    exit()

print("[INFO] CCTV IntelliGuard started...")
send_telegram_message("🔔 IntelliGuard Activated: CCTV monitoring started.")

while True:
    # Read raw frame from FFmpeg stdout
    raw_frame = pipe.stdout.read(width * height * 3)
    if len(raw_frame) < width * height * 3:
        print("[WARN] Frame not received, retrying...")
        time.sleep(0.5)
        continue

    # Convert raw bytes to BGR image
    frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))

    # store in circular buffer
    frame_buffer.append(frame.copy())

    # Step 1: motion detection
    motion = motion_detected(frame)

    # Step 2: YOLO detection
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
            record_frames = list(frame_buffer)
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
            send_telegram_message("✅ Motion ended. Video saved.")
            send_telegram_video(filename, caption="🎥 Event Recording")
            recording = False
            record_frames = []

    # Optional: show preview
    cv2.imshow("CCTV Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pipe.terminate()
cv2.destroyAllWindows()
send_telegram_message("🛑 IntelliGuard stopped.")
