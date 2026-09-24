import sys
import splashentry

conn, curr = splashentry.connect_to_database()
splashentry.fill_from_database(curr)
splashentry.splashScreen()

gameRunning = True
while gameRunning:
    gameRunning = splashentry.entryScreen(curr)

curr.close()
conn.close()
sys.exit()