#!/bin/bash
sudo apt update && sudo apt install -y python3-pip

# Uses python3 -m pip with --break-system-packages fallback for Debian 12+
python3 -m pip install --break-system-packages "psycopg[binary]" pygame 2>/dev/null || python3 -m pip install "psycopg[binary]" pygame

python3 main.py