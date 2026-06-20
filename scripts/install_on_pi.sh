#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip python3-opencv python3-picamera2 python3-rpi.gpio libcamera-apps
python3 -m venv .venv --system-site-packages
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp -n config.example.json config.json || true
mkdir -p dataset/owner models logs static
chmod +x scripts/*.sh
echo "Installed. Edit config.json then run: ./scripts/run.sh"
