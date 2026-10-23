import sys
import splashentry
import playaction
import MusicManager

conn, curr = splashentry.connect_to_database()
splashentry.splashScreen()

splash_entry = True
while splash_entry:
    splash_entry = splashentry.entryScreen(curr)
    
game_action = True
while game_action:
    # print("Game is running...")
    # playaction.start(splashentry.network, splashentry.redTeam, splashentry.greenTeam)
    game_action = playaction.playAction(splashentry.network, splashentry.redTeam, splashentry.greenTeam)

# Wait for the music track to end:
MusicManager.wait_until_finished()

# Only close everything after the music ends
curr.close()
conn.close()
sys.exit()