#!/bin/bash
sudo apt clean

sudo apt update

sudo apt install -y python3-pip --fix-missing

python3 -m pip install --break-system-packages "psycopg[binary]" pygame 2>/dev/null || python3 -m pip install "psycopg[binary]" pygame

python3 main.py