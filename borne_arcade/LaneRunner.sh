#!/bin/bash
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
command -v xdotool >/dev/null 2>&1 && timeout 0.2s xdotool mousemove 1280 1024 >/dev/null 2>&1 || true
cd "$ROOT_DIR/projet/LaneRunner"
python3.12 main.py
