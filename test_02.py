import cv2
import os

# Path to your video file (e.g., .mp4 or .avi)
video_path = os.path.join("videos", "sample.mp4")
print("Looking for video at:", os.path.abspath(video_path))

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("❌ Error opening video file.")
else:
    print("✅ Video opened successfully.")

# Read and display each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    cv2.imshow('Video Frame', frame)

    # Press 'q' to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release everything
cap.release()
cv2.destroyAllWindows()
