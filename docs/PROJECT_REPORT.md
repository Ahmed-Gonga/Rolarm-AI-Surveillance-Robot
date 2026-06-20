# Sleep Safe Robot - Completed Project Description

Sleep Safe Robot is a mobile-controlled Raspberry Pi security robot. The robot can move around the home, stream camera video to a phone, recognize enrolled family faces, mark unknown people as STRANGER, and trigger an alarm when danger is detected. It also reads gas, flame/fire, and PIR motion sensors.

## Main Features

1. Mobile web app installable on Android/iPhone as a PWA.
2. Owner PIN login.
3. Live camera stream.
4. Robot movement: forward, backward, left, right, stop.
5. Speed control through PWM pins ENA/ENB.
6. Face enrollment from the app.
7. LBPH face-recognition model training from the app.
8. EXIST versus STRANGER detection overlay on live video.
9. Alarm when stranger, gas, or fire is detected.
10. Event log stored in SQLite.
11. Telegram/email alert support through config.
12. Systemd service for automatic start on boot.
13. Mock mode for testing without real hardware.

## Suggested Hardware

- Raspberry Pi 4 or 5
- Raspberry Pi Camera Module or USB webcam
- 2 or 4 DC motors with robot chassis
- L298N motor driver
- MQ-2/MQ-5 gas sensor module with digital output
- Flame sensor module with digital output
- PIR motion sensor
- Active buzzer
- LED and resistor
- External battery for motors

## Workflow

1. Owner logs in from phone.
2. Owner controls the robot and checks live video.
3. Owner captures face samples for each child/family member.
4. Owner trains the recognition model.
5. System scans the camera feed continuously.
6. Known face = EXIST.
7. Unknown face = STRANGER and alarm/notification.
8. Gas/fire sensor = emergency alarm.

## Limitations

This is a complete graduation-project software package, but face recognition accuracy depends on camera quality, lighting, dataset quality, and hardware assembly. For real safety deployment, commercial-grade fire/gas alarms should still be used.
