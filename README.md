# 📹 CCTV IntelliGuard
CCTV IntelliGuard is an edge-based smart surveillance enhancement module designed to work with existing CCTV cameras. It detects and classifies human motion in real time while keeping power and processing requirements minimal.

The system uses OpenCV for lightweight motion pre-detection, activating a YOLOv8 model—optimized with quantization and pruning—only when movement is detected. This approach ensures efficient computation without compromising detection accuracy.

It is trained to identify whether a person is entering or exiting specific monitored areas such as classrooms, labs, and offices. When an event is detected, timestamped video clips are stored in Firestore, and alerts with clip links are sent to a connected mobile application via Firebase Cloud Messaging (FCM).

All processing is deployed on a Raspberry Pi, making it a compact, low-power, and cost-effective plug-in solution for upgrading existing CCTV systems.

---

## 📌 Problem Statement

Most existing CCTV systems continuously record footage without intelligence. This results in:
- No real-time alerts
- Inability to distinguish humans from general motion

---

## 🎯 Solution

Attach this **AI-based external hardware** to CCTV camera to:
- Detects human presence and captures a photo/video snippet of the individual.
- Sends captured images or video to registered mobile devices and directly to the device
- Triggers an alarm alert for unauthorized entries.
- Includes a manual alarm off switch for authorized overrides.

---

## Project Goals

- Automate monitoring during off-hours.
- Provide visual proof of entry (photo/video).
- Immediate notification to mobile devices and key personnel.
- Easy manual control (alarm ON/OFF button).
- Scalable for deployment across multiple university rooms.

---

## 🚀 Features

- Real-time detection of human motion  
- Works with existing cameras
- Sends video clip / photos with **timestamp** to a designated device  
- **Triggers an alarm** during restricted hours until manually turned off  
- Minimal hardware cost using **Raspberry Pi ( May be in future adds Coral USB Accelerator (can accelerate machine learning models)**
<img width="80" height="80" alt="image" src="https://github.com/user-attachments/assets/80b1483b-ab3e-4f76-a7f2-454aae308a86" />
 
 ---

## 🧰 Hardware Requirements


| Hardware            | Purpose                                              |
|---------------------|------------------------------------------------------|
| Surveillance Camera | For real-time image/video feed                       |
| Buzzer / Alarm      | To alert security on unauthorized entry              |
| Raspberry Pi        | For processing camera feed and sending notifications |
| Push Button         | Manual alarm off override                            |
| Smartphone / Tablet | To receive image or video alert                      |

---

## 🛠️ Software Stack ( Not finalize )


| Software / Library         | Role                                      |
|----------------------------|-------------------------------------------|
| Python / C++ / Node.js     | Backend logic and camera interface        |
| OpenCV                     | Human detection and image processing      |
| Twilio / Telegram API      | Sending automated alerts or messages in   |
|                            | your applications                         |
| FFmpeg                     |  For video clipping and compression       |
| MQTT / HTTP Server         | Communication between devices             |
| Real-Time Clock Scheduler  | To set active monitoring hours            |

- Frigate: Focused on efficient recording (clips and snapshots) only when motion and objects (like humans, cars) are detected.

---

## 🏗️ System Idea


<img width="300" height="1000" alt="Blank diagram" src="https://github.com/user-attachments/assets/5be20669-8b63-477c-8cda-1f50001fc7dd" />

---
---

## 🏗️ System Architecture


![ArcDia](https://github.com/user-attachments/assets/a0223083-38c3-434e-9bf3-c7cd0f91f38e)


---

## Real-World Application

- Designed to be deployed in university / office / school premises for surveillance.
- Helps in identifying unauthorized entries or suspicious activities. 
- Integrating an automated alarm system tailored for malls and public spaces to 
reduce the workload and required number of security personnel
  
---

## Future Improvements

- Face recognition for known vs unknown individuals.
- Remote access to live feed via secure portal.

---

## Status

-Stage 1: Initial concept & hardware planning  
-Stage 2: Camera setup and motion detection  
-Stage 3: Notification system development  
-Stage 4: System integration and field testing  

---

## 📅 Project Timeline – 14 Weeks

This section outlines the week-by-week development plan for the CCTV IntelliGuard system, focused on real-time human detection, video clipping, alerting, and scheduling.

---

### 🕐 Week 1: Finalize Requirements

* Define system features and workflow
* Determine active hours, alert rules, and UI expectations
* Confirm software stack and hardware specifications


### 🧾 Week 2: Procure Hardware

* Purchase Raspberry Pi, Camera Module, Buzzer, Push Button, SD card, and other essentials


### 🛠️ Week 3: CCTV feed

* Ask permission for CCTV
* Install necessary libraries: OpenCV, FFmpeg, etc.
* Try to access the cctv feed through the laptop


### 👁️ Week 4: Motion Detection (OpenCV)

* Frame differencing or background subtraction
* Filter out irrelevant motion (e.g., light, leaves)


### 🚶‍♂️ Week 5: Human Detection

* Integrate MobileNet SSD or YOLO
* Classify objects and filter only human presence


### 📟 Week 6 – Hardware & Basic Setup (1 week)
- Set up Raspberry Pi.
- Get HDMI/VNC connection to display Pi’s output on laptop.
- Connect CCTV feed and confirm Pi can stream and process video.


### 🧠 Weeks 7–10 – Model Training (4 weeks)
- Retrain/tune existing detection model to classify **direction of movement** (entering vs. leaving room).
- Collect labeled training data from CCTV footage.
- Train, validate, and deploy the updated model on Raspberry Pi.


### 📱 Weeks 11–12 – App & Storage Integration (2 weeks)
- Build mobile/desktop app interface for receiving alerts.
- Buffer frames on detection, assemble into short video clips.
- Store clips in Firestore with timestamps.
- Push notifications through the app.


### ✅ Weeks 13–14 – Final Testing & Documentation (2 weeks)
- Test full pipeline: detection → clip creation → storage → alert.
- Test under real-world conditions (different lighting, multiple people).
- Write final documentation, diagrams, and deployment guide.



