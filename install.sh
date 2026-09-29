sudo apt update

sudo apt install -y python3-venv

python3 -m venv env

source env/bin/activate

pip install "psycopg[binary]" pygame

python3 main.py
