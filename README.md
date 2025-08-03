# CCTV IntelliGuard

A smart hardware module that connects to any existing CCTV camera and performs real-time human detection using edge AI (AI algorithms directly on edge devices, like smartphones or IoT sensors, allowing real-time processing and decision-making without cloud reliance). This system can automatically trigger alarms, save video clips with timestamp, or send alerts to a designated phone number or messaging app based on specific conditions.

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

## 🏗️ System Architecture


<img width="300" height="1000" alt="Blank diagram" src="https://github.com/user-attachments/assets/5be20669-8b63-477c-8cda-1f50001fc7dd" />

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

---

### 🧾 Week 2: Procure Hardware

* Purchase Raspberry Pi, Camera Module, Buzzer, Push Button, SD card, and other essentials

---

### 🛠️ Week 3: Setup Raspberry Pi

* Flash Raspberry Pi OS
* Install necessary libraries: OpenCV, FFmpeg, etc.
* Validate camera feed and Pi GPIOs

---

### 👁️ Week 4: Motion Detection (OpenCV)

* Frame differencing or background subtraction
* Filter out irrelevant motion (e.g., light, leaves)

---

### 🚶‍♂️ Week 5: Human Detection (Edge AI)

* Integrate MobileNet SSD or YOLO-tiny
* Classify objects and filter only human presence

---

### 🔊 Week 6: Alarm Trigger System

* Activate buzzer during restricted hours on human detection
* GPIO programming for buzzer control

---

### 🛑 Week 7: Manual Override System

* Add physical push button to disable buzzer
* Test debounce and button state reading via GPIO

---

### 🎥 Week 8: Timestamped Video/Image Clip

* Use FFmpeg to save short video or snapshot on detection
* Save with human-readable timestamp for traceability

---

### ⏰ Week 9: RTC-Based Scheduling

* Implement real-time monitoring scheduler
* Monitor system only during configured restricted hours

---

### 📲 Week 10: Alert Notification System

* Integrate Telegram Bot or Twilio API
* Send image/video to registered users’ devices instantly

---

### 🧪 Week 11: AI Model Optimization

* Adjust confidence thresholds
* Reduce false alarms and missed detections

---

### ✅ Week 12: Alert Reliability Testing

* Simulate real-world conditions
* Ensure system sends consistent alerts without delay

---

### 🏫 Week 13: Field Testing

* Deploy system in selected real-world environment (e.g., university lab)
* Collect feedback, identify edge cases, improve reliability

---

### 📦 Week 14: Documentation & Packaging

* Finalize README, wiring diagram, and usage guide
* Clean and document code
* Package system for presentation or deployment

---

