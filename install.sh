pip install "psycopg[binary]"
pip install pygame

#Remove this chunk after everything gets connected
psql photon << 'EOF'
DELETE FROM Players WHERE ID > 1;
SELECT * FROM Players;
EOF
