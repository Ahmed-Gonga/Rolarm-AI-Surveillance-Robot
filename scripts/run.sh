#!/usr/bin/env bash
cd "$(dirname "$0")/.."
. .venv/bin/activate 2>/dev/null || true
python3 main.py
