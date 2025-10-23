import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque
import time
import os
import requests
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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
        time.sleep(3)
    print("[FAIL] Could not send Telegram message after retries.")

# ------------------------------
# GOOGLE DRIVE CONFIGURATION
# ------------------------------
def setup_drive():
    """Authenticate with Google Drive and return drive object"""
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:
        print("🔐 No credentials found. Opening Google authentication link...")
        gauth.CommandLineAuth()
    elif gauth.access_token_expired:
        print("🔄 Token expired. Refreshing...")
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    return GoogleDrive(gauth)

# Initialize Google Drive once
drive = setup_drive()

# Folder ID for CCTV IntelliGuard folder
FOLDER_ID = "1dDQVhGP191-cgVVfep99DoRllymQLqV4"

def upload_to_drive(video_path):
    """Upload a video file to Google Drive folder"""
    if not os.path.exists(video_path):
        print(f"[ERROR] File not found for upload: {video_path}")
        return False

    filename = os.path.basename(video_path)
    print(f"[INFO] Uploading {filename} to Google Drive...")

    try:
        file_drive = drive.CreateFile({
            'title': filename,
            'parents': [{'id': FOLDER_ID}]
        })
        file_drive.SetContentFile(video_path)
        file_drive.Upload()
        print("[INFO] ✅ Upload successful to Google Drive.")
        return True
    except Exception as e:
        print(f"[ERROR] Google Drive upload failed: {e}")
        return False

# ------------------------------
# CCTV CONFIGURATION
# ------------------------------
model = YOLO('yolov8s.pt')
url = "rtsp://student1:Stu1%40cse@10.8.104.13:554/Streaming/Channels/102?tcp"

ffmpeg_cmd = [
    "ffmpeg",
    "-i", url,
    "-f", "rawvideo",
    "-pix_fmt", "bgr24",
    "-vsync", "0",
    "-"
]
pipe = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

width, height = 640, 480
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=True)
frame_buffer = deque(maxlen=125)

recording = False
record_frames = []
cooldown = 250
frames_after_motion = 0
SAVE_DIR = "recorded_events_upgrade_lab"
os.makedirs(SAVE_DIR, exist_ok=True)

def motion_detected(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)
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
    raw_frame = pipe.stdout.read(width * height * 3)
    if len(raw_frame) < width * height * 3:
        print("[WARN] Frame not received, retrying...")
        time.sleep(0.5)
        continue

    frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))
    frame_buffer.append(frame.copy())
    motion = motion_detected(frame)

    human_detected = False
    if motion:
        results = model(frame, verbose=False)
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if model.names[cls] == "person":
                    human_detected = True
                    break

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
            send_telegram_message("✅ Motion ended. Video saved. Uploading to Drive...")
            success = upload_to_drive(filename)
            if success:
                send_telegram_message("📤 Video successfully uploaded to Google Drive folder.")
            else:
                send_telegram_message("⚠️ Upload failed. Check system logs.")
            recording = False
            record_frames = []

    cv2.imshow("CCTV Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pipe.terminate()
cv2.destroyAllWindows()
send_telegram_message("🛑 IntelliGuard stopped.")
