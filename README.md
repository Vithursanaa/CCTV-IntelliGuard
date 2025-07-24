# AI-Powered Human Detection Module for CCTV Systems

A smart hardware module that connects to any existing CCTV camera and performs **real-time human detection** using edge AI. This system can automatically trigger alarms, save video clips, or send alerts to a designated phone number or messaging app based on specific conditions.

---

## 📌 Problem Statement

Most existing CCTV systems continuously record footage without intelligence. This results in:
- No real-time alerts
- Inability to distinguish humans from general motion

---

## 🎯 Solution

Attach this **AI-based external hardware** to any USB or IP CCTV camera to:
- Detects human presence and captures a photo/video snippet of the individual.
- Triggers an alarm alert for unauthorized entries.
- Sends captured images or video to registered mobile devices and directly to the 	Responsible Director of the Institute.
- Includes a manual alarm off switch for authorized overrides.
- Monitors only during off-time (non-working hours) of the university.

---

Project Goals

- Automate monitoring during off-hours.
- Provide visual proof of entry (photo/video).
- Immediate notification to mobile devices and key personnel.
- Easy manual control (alarm ON/OFF button).
- Scalable for deployment across multiple university rooms.

---

## 🚀 Features

✅ Real-time detection of human motion  
✅ Works with existing **USB or IP cameras (RTSP supported)**  
✅ Sends video clip with **timestamp** to a designated device  
✅ **Triggers an alarm** during restricted hours until manually turned off  
✅ Minimal hardware cost using **Raspberry Pi + Coral USB Accelerator**  
✅ Optional support for **Telegram alerts or Email notifications**

---

## 🧰 Hardware Requirements

| Hardware            | Purpose                                              |
|---------------------|------------------------------------------------------|
| Surveillance Camera | For real-time image/video feed                       |
| Buzzer / Alarm      | To alert security on unauthorized entry              |
| Raspberry Pi        | For processing camera feed and sending notifications |
| Push Button         | Manual alarm off override                            |
| Smartphone / Tablet | To receive image or video alert                      |

Use existing CCTV cameras if they support IP streaming.

---

## 🛠️ Software Stack

| Software / Library         | Role                                      |
|----------------------------|-------------------------------------------|
| Python / C++ / Node.js     | Backend logic and camera interface        |
| OpenCV                     | Human detection and image processing      |
| Twilio / Telegram API      | Send alerts and images to mobile devices  |
| FFmpeg                     | For video clipping and compression        |
| MQTT / HTTP Server         | Communication between devices             |
| Real-Time Clock Scheduler  | To set active monitoring hours            |

---

## 🏗️ System Architecture
           ┌──────────────────────┐
           │ CCTV Camera (USB/IP) │
           └──────────┬───────────┘
                      |
                      ▼
        ┌───────────────────────────┐
        │ Raspberry Pi + Coral Edge │
        │ with Frigate Detection    │
        └────────────┬──────────────┘
                     │
              ┌──────▼─────────┐
              │ Human Detected │
              └──────┬─────────┘
                     │
        ┌────────────▼─────────────┐
        │ Save Clip + Timestamp    │
        └────────────┬─────────────┘
                     │
        ┌────────────▼─────────────┐
        │ Send Alert (Telegram)    │
        └────────────┬─────────────┘
                     │
        ┌────────────▼────────────────────┐
        │ If Restricted Hours             │
        │ Ring Alarm Until Turned Off     │
        └─────────────────────────────────┘

---

Setup Instructions

1. Install required packages (OpenCV, Python libraries, etc.).
2. Connect your camera module or IP stream to your device.
3. Configure working hours in the code to enable after-hours monitoring.
4. Integrate alert system with Twilio/Telegram using API credentials.
5. Deploy the system on Raspberry Pi or other microcontroller.
6. Test alert, video capture, and notification features thoroughly.

---

Real-World Application

- Designed to be deployed in university premises for post-classroom surveillance.
- Helps in identifying unauthorized entries or suspicious activities.
- Can be extended to lab areas, equipment rooms, and hostel corridors at the night hours.

---

Future Improvements

- Face recognition for known vs unknown individuals.
- Remote access to live feed via secure portal.
- Battery backup and offline storage.
- Integration with access control (RFID, biometric).

---

Status

-Stage 1: Initial concept & hardware planning  
-Stage 2: Camera setup and motion detection  
-Stage 3: Notification system development  
-Stage 4: System integration and field testing  

---

# 📅 10-Week Project Timeline

This timeline outlines the structured development of the **AI-Powered Human Detection Module for CCTV Systems**, with a balanced weekly workload. Each week builds upon the last, leading to a fully functional, deployable, and scalable surveillance solution.

---

## 🗓️ Weekly Development Plan

### **Week 1: Project Kickoff & Environment Setup**

**Goals:**
- Define project requirements and install core tools

**Tasks:**
- [ ] Finalize system architecture
- [ ] List hardware/software requirements
- [ ] Set up Raspberry Pi OS with Python
- [ ] Enable SSH, configure Wi-Fi, and install essential packages
- [ ] Initialize Git repository and folder structure

---

### **Week 2: Camera Setup & Basic Video Stream**

**Goals:**
- Connect CCTV (USB/IP) and stream video

**Tasks:**
- [ ] Connect USB or RTSP-based IP camera
- [ ] Stream live video using OpenCV
- [ ] Display frame with timestamp overlay
- [ ] Test video feed performance (FPS, latency)

---

### **Week 3: Motion Detection & Video Capture**

**Goals:**
- Implement motion detection and clip saving

**Tasks:**
- [ ] Detect motion using frame differencing
- [ ] Capture short video clips on motion detection
- [ ] Add timestamp to filenames
- [ ] Use FFmpeg for video compression

---

### **Week 4: Human Detection Using Coral TPU**

**Goals:**
- Detect humans using Edge AI

**Tasks:**
- [ ] Install Coral Edge TPU runtime
- [ ] Integrate Frigate or TFLite human detection model
- [ ] Display bounding boxes for detected persons
- [ ] Filter out non-human movement

---

### **Week 5: Alarm System & Push Button Integration**

**Goals:**
- Add buzzer alarm and manual override

**Tasks:**
- [ ] Connect buzzer to GPIO pin
- [ ] Add push button for alarm control
- [ ] Trigger alarm on detection during off-hours
- [ ] Implement GPIO debounce for button

---

### **Week 6: Real-Time Clock (RTC) & Schedule Logic**

**Goals:**
- Enable off-hour surveillance only

**Tasks:**
- [ ] Install RTC module
- [ ] Configure restricted monitoring hours
- [ ] Enable detection only during specified times
- [ ] Log all detection events with timestamps

---

### **Week 7: Alert System (Telegram / Twilio Integration)**

**Goals:**
- Notify security via messaging apps

**Tasks:**
- [ ] Set up Telegram Bot or Twilio API
- [ ] Send photo/video alert with timestamp
- [ ] Add retry and error handling
- [ ] Log alerts and delivery status

---

### **Week 8: Storage, Auto-Start & Optimization**

**Goals:**
- Make the system persistent and efficient

**Tasks:**
- [ ] Save media clips in organized folders
- [ ] Set up auto-start using systemd or cron
- [ ] Optimize detection threshold and performance
- [ ] Add exception handling for API/camera errors

---

### **Week 9: Field Testing & Deployment**

**Goals:**
- Deploy and validate in a real environment

**Tasks:**
- [ ] Deploy in a selected university room or lab
- [ ] Conduct tests during night/off-hours
- [ ] Collect feedback and adjust parameters
- [ ] Evaluate detection reliability and false alerts

---

### **Week 10: Documentation & Final Review**

**Goals:**
- Finalize the system and plan future scalability

**Tasks:**
- [ ] Write installation and usage documentation
- [ ] Create demo video (optional)
- [ ] Document code and configuration files
- [ ] Suggest enhancements and deployment roadmap

---

## 🚀 Future Enhancements

- Face recognition for authorized personnel
- Remote access via secure web interface
- Battery backup and offline clip storage
- Integration with RFID or biometric systems
- Cloud alert syncing and mobile dashboard

---


