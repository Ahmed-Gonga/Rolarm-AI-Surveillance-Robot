# Rolarm AI Surveillance Robot

An intelligent AI-powered home security robot designed for real-time monitoring, remote navigation, and environmental safety. Built using Raspberry Pi, Computer Vision, IoT sensors, and a mobile-first control interface, Rolarm combines autonomous surveillance with smart home protection in a single integrated platform.

## Overview

Rolarm is a smart surveillance robot capable of remotely patrolling indoor environments while providing live video monitoring, face recognition, intrusion detection, and safety alerts. The system enables homeowners to monitor their homes from anywhere and receive notifications when unfamiliar individuals or hazardous environmental conditions are detected.

## Key Features

### Computer Vision & AI

* Real-time face detection and recognition
* Known-person identification
* Stranger detection and alert generation
* Face enrollment and model training workflow
* Live camera streaming

### Mobile Monitoring & Control

* Mobile-friendly Progressive Web Application (PWA)
* Remote robot navigation
* Real-time system monitoring
* Secure owner authentication
* Event and alert history

### Safety & Security

* Gas leak detection
* Flame/fire detection
* Motion detection using PIR sensors
* Audible alarm and visual warning indicators
* Emergency notification support

### Robotics & Hardware

* Raspberry Pi based architecture
* L298N motor driver integration
* Camera module support
* Buzzer and LED indicators
* Expandable sensor framework

### Data & Logging

* SQLite event database
* Incident logging
* Alert history management
* Sensor activity tracking

## System Architecture

The system consists of four primary layers:

1. **Mobile Application Layer**

   * User authentication
   * Remote control dashboard
   * Live monitoring interface

2. **Application Layer**

   * Flask backend
   * Alert management
   * Event logging
   * API services

3. **AI Layer**

   * Face recognition
   * Stranger detection
   * Image processing

4. **Hardware Layer**

   * Raspberry Pi
   * Camera module
   * Gas sensor
   * Flame sensor
   * PIR sensor
   * Motor driver
   * Alarm system

## Technology Stack

* Python
* Flask
* OpenCV
* SQLite
* HTML/CSS/JavaScript
* Raspberry Pi
* L298N Motor Driver
* IoT Sensors

## Installation

```bash
git clone https://github.com/Ahmed-Gonga/Rolarm-AI-Surveillance-Robot.git
cd Rolarm-AI-Surveillance-Robot

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 main.py
```

## Access

Open the application locally:

```text
http://localhost:5000
```

Or from a device connected to the same network:

```text
http://<RASPBERRY_PI_IP>:5000
```

## Project Purpose

This project was developed as an extension and enhancement of a smart home security graduation project concept. The objective is to integrate robotics, computer vision, IoT sensing, and mobile accessibility into a unified security platform capable of monitoring homes and notifying owners of potential threats or hazards.

## Future Improvements

* Deep-learning based face recognition
* Cloud synchronization
* Mobile native application
* Autonomous navigation
* Object detection
* Multi-camera support
* Voice assistant integration

## License

This project is intended for educational, research, and prototyping purposes.

## Author

Ahmed Wahba

- GitHub: https://github.com/Ahmed-Gonga
- LinkedIn: https://linkedin.com/in/ahmedhwahba
