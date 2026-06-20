# Sleep Safe Robot - Full Raspberry Pi Project

A completed Raspberry Pi graduation project: mobile-controlled home security robot with camera streaming, face recognition, gas/fire detection, alarm, event history, and alerts.

## What is included

- Flask backend API
- Mobile web app / PWA
- Camera live stream
- Face enrollment and training
- EXIST / STRANGER detection
- Robot motor movement using L298N
- Gas, flame/fire, and PIR sensor support
- Buzzer and LED alarm
- SQLite event database
- Telegram/email alert hooks
- Systemd auto-start service
- Full wiring and report documentation

## Install on Raspberry Pi

```bash
unzip sleep_safe_robot_full.zip
cd sleep_safe_robot_full
./scripts/install_on_pi.sh
nano config.json
./scripts/run.sh
```

Open on your phone:

```text
http://RASPBERRY_PI_IP:5000
```

Default PIN is `1234`. Change it in `config.json`.

## First use

1. Connect Pi and phone to the same Wi-Fi.
2. Open the app in the phone browser.
3. Login with the PIN.
4. Put one family member in front of the camera.
5. Type their name and press **Capture Face** many times until you have at least 20 images. Use different angles and lighting.
6. Press **Train Model**.
7. Known people show as `EXIST: name`; unknown faces show `STRANGER`.

## Run automatically on boot

```bash
./scripts/create_service.sh
```

## Test without hardware

Edit `config.json`:

```json
"mock_hardware": true,
"mock_camera": true
```

Then run:

```bash
python3 main.py
```

## Important safety note

This is a graduation-project/home prototype. It can alert you, but it must not replace certified fire or gas safety equipment.
