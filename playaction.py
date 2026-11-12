import pygame # type: ignore -> Just so we don't have constantly get an import warning.
import sys
import psycopg # type: ignore
from SocketManager import SocketManager # Custom networking class.

pygame.font.init()

GAME_MINUTES = 6
GAME_LENGTH = GAME_MINUTES * 60 # Game length in seconds 

# Colors
blackRGB     = (0, 0, 0)
whiteText    = (255, 255, 255)
borderYellow = (230, 230, 60)
titleCyan    = (80, 200, 235)
redText      = (255, 140, 140)
greenText    = (140, 255, 140)

# Fonts
headerFont = pygame.font.Font(None, 40) # RED TEAM / GREEN TEAM
boxTitleFont = pygame.font.Font(None, 34) # "Current Scores" / "Current Game Action"
playerFont = pygame.font.Font(None, 24) # Player names and scores
timerFont = pygame.font.Font(None, 40) # Time Remaining
actionFont = pygame.font.Font(None, 24) # Lines inside the game action window
hintFont = pygame.font.Font(None, 20) # For post game options hints

# Layout
scoresBox = pygame.Rect(20, 25, 960, 335)
actionBox = pygame.Rect(20, 370, 960, 175)
timerBox  = pygame.Rect(20, 555, 960, 55)

ROW_START_Y = 80   # Y of the first player row.
ROW_HEIGHT  = 17   # 15 rows * 17px fits above the team totals.
TOTAL_Y     = 337  # Y of the team total score row.

# Column positions: (name x, score right edge x)
redNameX,   redScoreX   = 45, 465
greenNameX, greenScoreX = 515, 955


clock = pygame.time.Clock()
startTime = None          # Set on the first call to playAction().
playerScores = {}         # {"playerID": score}. Nothing updates this yet, so everyone shows 0.
eventLog = []             # Empty for now (no events yet).
actionBackground = pygame.Surface((actionBox.width - 6, actionBox.height - 6))
gameOver = False            # Flag to indicate if the game is over.
endBroadcastSent = False      # Flag to indicate if the end game broadcast has been sent.


def draw_titled_box(screen, rect, title):
    # Yellow box with a title sitting on the top right of the border.
    pygame.draw.rect(screen, borderYellow, rect, width=3)
    titleSurface = boxTitleFont.render(title, True, titleCyan)
    titleRect = titleSurface.get_rect(midright=(rect.right - 25, rect.top))
    pygame.draw.rect(screen, blackRGB, titleRect.inflate(12, 0)) # Black patch so the border doesn't run through the text.
    screen.blit(titleSurface, titleRect)


def draw_team(screen, team, nameX, scoreRightX, color):
    # Draws every player that has been fully entered (ID + codename) and returns the team total.
    rows = []
    for player in team:
        playerID, codename = player[0], player[1]
        if playerID is not None and codename is not None:
            rows.append((str(codename), playerScores.get(str(playerID), 0)))

    rows.sort(key=lambda row: row[1], reverse=True) # Highest score on top.

    for index, (codename, score) in enumerate(rows):
        y = ROW_START_Y + index * ROW_HEIGHT
        nameSurface = playerFont.render(codename, True, color)
        scoreSurface = playerFont.render(str(score), True, color)
        screen.blit(nameSurface, (nameX, y))
        screen.blit(scoreSurface, scoreSurface.get_rect(topright=(scoreRightX, y)))

    total = sum(score for _, score in rows)
    totalSurface = playerFont.render(str(total), True, color)
    screen.blit(totalSurface, totalSurface.get_rect(topright=(scoreRightX, TOTAL_Y)))
    return total


def format_time(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}" # Makes sure that seconds is always represented by two digits so we get 6:07 instead of 6:7


def reset_game():
    global startTime, playerScores, eventLog, gameOver, endBroadcastSent
    startTime = None
    playerScores.clear()
    eventLog.clear()
    gameOver = False
    endBroadcastSent = False
    pygame.display.set_caption("Entry Terminal")


# Recieve Incoming Data:
def recieve_action_data(network: SocketManager):
    while True:
        received_data = network.receive()
        if received_data is None: # No data currently received.
            break
        try:
            # Process Data:
            shooterID, taggedID = received_data.split(":") # Splits recieved data into required IDs.
            shooterID = int(shooterID)
            taggedID = int(taggedID)
            # Send Data to Action Function:
            handle_action(shooterID, taggedID)
        except ValueError:
            print(f"Invalid data received: {received_data}") # This shouldn't happen but it's here just in case hardware or generator produce unexpected values.

# Handle Incoming Actions:
def handle_action(shooterID, taggedID):
    print(f"Shooter ID: {shooterID} tagged Target ID: {taggedID}") # Example printing for recieving tests.

    ###################################
    # ALL ACTION LOGIC SHOULD GO HERE #
    ###################################

def playAction(network: SocketManager, redTeam, greenTeam) -> int:
    global startTime, actionBackground, gameOver, endBroadcastSent
    screen = pygame.display.get_surface()

    # First frame setup
    if startTime is None:
        pygame.display.set_caption("Play Action")
        startTime = pygame.time.get_ticks()
        gameOver = False
        endBroadcastSent = False

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            return -1  # Exit the main loop and quit the game.
        
        if gameOver:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F10:
                    pygame.mixer.music.stop()
                    reset_game()
                    return 1  # Return to the entry screen without quitting the game.
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return -1  # Exit the main loop and quit the game.

    # Timer
    elapsed = (pygame.time.get_ticks() - startTime) // 1000
    remaining = max(0, GAME_LENGTH - elapsed)
    
    if remaining <= 0:
        remaining = 0
        if not endBroadcastSent:
            for _ in range(3):
                network.broadcast_game("221")  # Stop code from "photon-main\udp_files\python_trafficgenerator readme.txt"
            endBroadcastSent = True
            gameOver = True  # Set the game over flag to True when time runs out.

    # Recieve Data:
    recieve_action_data(network)

    # Background
    screen.fill(blackRGB)

    # Scores window 
    draw_titled_box(screen, scoresBox, "Current Scores")

    redHeader = headerFont.render("RED TEAM", True, whiteText)
    greenHeader = headerFont.render("GREEN TEAM", True, whiteText)
    screen.blit(redHeader, redHeader.get_rect(midtop=(255, 40)))
    screen.blit(greenHeader, greenHeader.get_rect(midtop=(735, 40)))

    draw_team(screen, redTeam, redNameX, redScoreX, redText)
    draw_team(screen, greenTeam, greenNameX, greenScoreX, greenText)

    # Game action window
    screen.blit(actionBackground, (actionBox.x + 3, actionBox.y + 3))
    draw_titled_box(screen, actionBox, "Current Game Action")

    # Most recent events at the bottom. Nothing gets added to eventLog yet.
    maxLines = (actionBox.height - 20) // 20
    for index, line in enumerate(eventLog[-maxLines:]):
        lineSurface = actionFont.render(line, True, whiteText)
        screen.blit(lineSurface, (actionBox.x + 15, actionBox.y + 12 + index * 20))

    # Time remaining 
    pygame.draw.rect(screen, borderYellow, timerBox, width=3)
    timerSurface = timerFont.render("Time Remaining:  " + format_time(remaining), True, whiteText)
    screen.blit(timerSurface, timerSurface.get_rect(midright=(timerBox.right - 40, timerBox.centery)))
    
    # Draw hints for post-game options if the game is over
    if gameOver:
        hints_text = "[F10] Return to Player Entry Screen  |  [ESC] Exit Game"
        hints_render = hintFont.render(hints_text, True, (200, 200, 200)) # Light gray text
        screen.blit(hints_render, hints_render.get_rect(midleft=(timerBox.left + 25, timerBox.centery)))

    # Screen updates
    pygame.display.flip()
    clock.tick(30)
    
    return 3  # Continue the play action screen without quitting the game.