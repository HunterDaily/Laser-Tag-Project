#!/bin/bash

# 1. Point sources.list to the Debian archive instead of the live mirrors
sudo sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list
sudo sed -i 's|security.debian.org/debian-security|archive.debian.org/debian-security|g' /etc/apt/sources.list

# 2. Disable the updates repository (this usually does not exist in the archive)
sudo sed -i '/bullseye-updates/s/^/#/' /etc/apt/sources.list

# 3. Tell apt to ignore the expiration date of the archived repositories
echo 'Acquire::Check-Valid-Until "false";' | sudo tee /etc/apt/apt.conf.d/99archive

# 4. Clean the broken cache and fetch the new archive lists
sudo apt clean
sudo apt update

# 5. Install pip and the required python packages
sudo apt install -y python3-pip
python3 -m pip install --break-system-packages "psycopg[binary]" pygame 2>/dev/null || python3 -m pip install "psycopg[binary]" pygame

python3 main.py