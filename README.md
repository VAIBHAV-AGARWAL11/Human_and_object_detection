# AI-Based Human Detection Monitoring System for Industrial Surveillance..

> An AI-powered real-time human detection, tracking, and automated alert system developed during my **Summer Internship at Hindustan Zinc Limited**.

---

##  Project Overview

The **AI-Based Human Detection Monitoring System** is a real-time computer vision application designed to automate human presence monitoring through a live camera feed.

The system uses **YOLOv8** for human detection and tracking and **OpenCV** for camera capture, image processing, and visualization. When a person is detected, the system assigns a unique tracking ID and monitors the detected individual across successive frames.

The system can automatically generate a security alert when a detection event occurs. It captures an annotated screenshot of the detection, saves the image locally, and sends an automated email notification with the captured image attached.

This project was developed as part of my **Summer Internship at Hindustan Zinc Limited** and demonstrates the practical application of **Artificial Intelligence, Computer Vision, Deep Learning, Real-Time Video Processing, Object Tracking, and Automated Notification Systems** in an industrial surveillance context.

---

##  Objectives

The primary objectives of the project are:

- Automate human presence detection from camera feeds.
- Reduce dependency on continuous manual CCTV monitoring.
- Track detected individuals using unique tracking IDs.
- Capture visual evidence when a detection event occurs.
- Automatically notify designated personnel through email.
- Maintain controlled and repeated alert mechanisms.
- Improve the efficiency and responsiveness of surveillance systems.
- Demonstrate the application of AI-based computer vision in industrial environments.

---

##  Industrial Application

In industrial environments, continuous surveillance of specific areas can be important for security and operational monitoring.

Traditional CCTV systems generally require personnel to continuously observe multiple screens. This system introduces an AI-based monitoring layer that can automatically identify human presence and initiate an alert workflow.

### Potential Applications

- Restricted-area monitoring
- Industrial facility surveillance
- Security monitoring
- Control-room surveillance
- Human presence detection
- Automated incident notification
- Facility access monitoring
- Safety-related monitoring scenarios

---

##  System Workflow

```text
                ┌───────────────────────┐
                │    Live Camera Feed   │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │      YOLOv8 Model     │
                │   Human Detection     │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Human Tracking & ID   │
                │ Assignment            │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Detection Event       │
                │ Processing             │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Annotated Screenshot  │
                │ Capture                │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Alert Processing      │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Automated Email Alert │
                │ + Screenshot          │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Concerned Authority   │
                │ Receives Notification │
                └───────────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Monitoring Continues  │
                └───────────────────────┘
