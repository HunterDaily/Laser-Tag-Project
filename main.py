import sys
import splashentry

conn, curr = splashentry.connect_to_database()
splashentry.splashScreen()

splash_entry = True
while splash_entry:
    splash_entry = splashentry.entryScreen(curr)
    
game_action = True
while game_action:
    print("Game is running...")
    # playaction.start(splashentry.network, splashentry.redTeam, splashentry.greenTeam)
    break # Placeholder for the actual game loop. Replace with game logic.

curr.close()
conn.close()
sys.exit()