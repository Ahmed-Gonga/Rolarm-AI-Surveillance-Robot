#!/usr/bin/env bash
set -e
PROJECT_DIR=$(cd "$(dirname "$0")/.." && pwd)
SERVICE=/etc/systemd/system/sleep-safe-robot.service
sudo tee $SERVICE >/dev/null <<EOF
[Unit]
Description=Sleep Safe Robot Raspberry Pi Server
After=network.target

[Service]
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/.venv/bin/python $PROJECT_DIR/main.py
Restart=always
User=$USER
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable sleep-safe-robot
sudo systemctl restart sleep-safe-robot
systemctl status sleep-safe-robot --no-pager
