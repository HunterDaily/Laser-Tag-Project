import sys
import splashentry
import playaction
import MusicManager

conn, curr = splashentry.connect_to_database()

SCREEN_SPLASH = 0
SCREEN_ENTRY = 1
SCREEN_COUNTDOWN = 2
SCREEN_PLAY = 3
SCREEN_QUIT = -1
currScreen = SCREEN_SPLASH
quitGame = False

while not quitGame:
    if currScreen == SCREEN_SPLASH:
        splashentry.splashScreen()
        currScreen = SCREEN_ENTRY
    elif currScreen == SCREEN_ENTRY:
        currScreen = splashentry.entryScreen(curr)
    elif currScreen == SCREEN_COUNTDOWN:
        splashentry.countDown()
        currScreen = SCREEN_PLAY
    elif currScreen == SCREEN_PLAY:
        currScreen = playaction.playAction(splashentry.network, splashentry.redTeam, splashentry.greenTeam)
    else:
        quitGame = True

# Wait for the music track to end:
MusicManager.wait_for_track_finished()

# Only close everything after the music ends
curr.close()
conn.close()
sys.exit()