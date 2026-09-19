import pygame
import sys
import psycopg # type: ignore -> Just so we don't have constantly get an import warning.
from SocketManager import SocketManager # Custom networking class.

# Initialize socket manager
network = SocketManager()

# Network Popup Variables:
networkPopup = False
networkAddress = "127.0.0.255" # Default broadcast address.

# Popup function to draw network & later other popups:
def draw_popup(input_text, description):
    # Main Box:
    pygame.draw.rect(gameScreen, blackRGB, (250, 200, 500, 225))
    # Prompt Text:
    prompt = playerFont.render(description, True, blueTitle)
    gameScreen.blit(prompt, (260, 210))
    # Input Box:
    pygame.draw.rect(gameScreen, whiteText, (260, 250, 480, 30))
    # Input Text:
    input_text_render = playerFont.render(input_text, True, blackRGB)
    gameScreen.blit(input_text_render, (260, 250))


#Connect to database
conn = ""
try:
    conn = psycopg.connect(dbname="photon")
    curr = conn.cursor()
    conn.autocommit = True
except Exception as e:
    print(f"An error occurred: {e}")

pygame.init()

#entry screen window size variables
windowWidth = 1000
windowHeight = 625 # Previously 750, I'm adjusting to better fit the spashscreen logo's size ratio.

#entry screen window using the window size variable
gameScreen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Entry Terminal")

#Splash screen 
#logo = pygame.image.load("photon-main\logo.jpg") #Use on Windows machines
logo = pygame.image.load("photon-main/logo.jpg") #Use on Linux machines
logo = pygame.transform.scale(logo, (1000, 625)) # Logo is weirdly 3487 by 2221 originally, somewhat close to a 16:10 ratio. Original sizing was to 800 and 400.


#colors to make the player entry screen.
blackRGB        = (0, 0, 0)
blueTitle       = (102, 102, 255)
redBack         = (60, 0, 0)
greenBack       = (0, 60, 0)
whiteText       = (255, 255, 255)

#fonts for the entry screen
titleFont = pygame.font.Font(None, 30)
teamNames = pygame.font.Font(None, 25)
columnFont = pygame.font.Font(None, 25)
playerFont = pygame.font.Font(None, 25)

#variable to make sure the entry screen is still running.
gameRunning     = True

#selecting rows/teams variables
rowSelector     = 0
teamSelector    = "red"

#arrays for storing player's names/equipment ID
redTeam     = []
greenTeam   = []
#making it into 15 elements with name/equipment ID for each team
for numPlayers in range(15):
    redTeam.append([None, None])
    greenTeam.append([None, None])
typingCheck = False
keyInput    = ""
inputMode   = 0
counter = 0

#Imports rows from database
curr.execute("SELECT * FROM Players;")
for Row in curr.fetchall():
	if Row[0] <= len(redTeam):
		redTeam[Row[0]-1] = [Row[1], None]
	elif Row[0] <= (len(redTeam) + len(greenTeam)):
		greenTeam[Row[0]-16] = [Row[1], None]
typingCheck = False

def entryScreen():
    global gameRunning, rowSelector, teamSelector, typingCheck, keyInput, inputMode, redTeam, greenTeam # Original player entry variables.
    global networkPopup, networkAddress # Network popup variables.

    #background color
    gameScreen.fill(blackRGB)
    #background color for the teams
    pygame.draw.rect(gameScreen, redBack, (125, 45, 375, 500))
    pygame.draw.rect(gameScreen, greenBack, (500, 45, 375, 500))
    
    #entry screen title
    gameTitle = titleFont.render("Edit Current Game", True, blueTitle)
    gameScreen.blit(gameTitle, (405, 15))

    #entry screen team titles
    redTitle    = teamNames.render("RED TEAM", True, whiteText)
    greenTitle  = teamNames.render("GREEN TEAM", True, whiteText) 
    gameScreen.blit(redTitle, (265, 50))
    gameScreen.blit(greenTitle, (615, 50))

    #for loop to make rows of white boxes for red/green team
    for numRows in range(15):
        rowsY = 75 + (numRows * 30)
            
        #arrow selector to pick a row to put player name/equipment ID in red/green teams
        if numRows == rowSelector:
            selectArrow = columnFont.render(">>", True, whiteText)
            if teamSelector == "red":
                gameScreen.blit(selectArrow, (120, rowsY))
            elif teamSelector == "green":
                gameScreen.blit(selectArrow, (495, rowsY))
        playerNumber = columnFont.render(str(numRows+1), True, whiteText)
        #red team table
        gameScreen.blit(playerNumber, (145, rowsY))
        pygame.draw.rect(gameScreen, whiteText, (175, rowsY, 120, 25))
        pygame.draw.rect(gameScreen, whiteText, (300, rowsY, 180, 25))
        #green team table
        gameScreen.blit(playerNumber, (520, rowsY))
        pygame.draw.rect(gameScreen, whiteText, (550, rowsY, 120, 25))
        pygame.draw.rect(gameScreen, whiteText, (675, rowsY, 180, 25))

        #displays the player names/equipment ID for red/green teams
        #Red Team names/equipment ID
        if redTeam[numRows][0] is not None:
            if not (numRows == rowSelector and teamSelector == "red" and typingCheck == True and inputMode == 0):
                playerName = playerFont.render(str(redTeam[numRows][0]), True, blackRGB)
                gameScreen.blit(playerName, (180, rowsY + 5))
        if redTeam[numRows][1] is not None:
            if not (numRows == rowSelector and teamSelector == "red" and typingCheck == True and inputMode == 1):
                equipID = playerFont.render(str(redTeam[numRows][1]), True, blackRGB)
                gameScreen.blit(equipID, (305, rowsY + 5))
        #Green Team names/equipment ID
        if greenTeam[numRows][0] is not None:
            if not (numRows == rowSelector and teamSelector == "green" and typingCheck == True and inputMode == 0):
                playerName = playerFont.render(str(greenTeam[numRows][0]), True, blackRGB)
                gameScreen.blit(playerName, (555, rowsY + 5))
        if greenTeam[numRows][1] is not None:
            if not (numRows == rowSelector and teamSelector == "green" and typingCheck == True and inputMode == 1):
                equipID = playerFont.render(str(greenTeam[numRows][1]), True, blackRGB)
                gameScreen.blit(equipID, (680, rowsY + 5))
            
        #displays players names/equipment ID while being typed
        if numRows == rowSelector and typingCheck == True:
            if teamSelector == "red":
                if inputMode == 0:
                    playerName = playerFont.render(keyInput, True, blackRGB)
                    gameScreen.blit(playerName, (180, rowsY + 5))
                elif inputMode == 1:
                    equipID = playerFont.render(keyInput, True, blackRGB)
                    gameScreen.blit(equipID, (305, rowsY + 5))
            elif teamSelector == "green":
                if inputMode == 0:
                    playerName = playerFont.render(keyInput, True, blackRGB)
                    gameScreen.blit(playerName, (555, rowsY + 5))
                elif inputMode == 1:
                    equipID = playerFont.render(keyInput, True, blackRGB)
                    gameScreen.blit(equipID, (680, rowsY + 5))


    #checks for key events or closing window
    for event in pygame.event.get():

        #checks to see if user uses presses a key
        if event.type == pygame.KEYDOWN:
                
            # Network Popup Toggle:
            if event.key == pygame.K_F1: # Currently using F1 because we were given zero direction on what key to use, even though I believe F1 may end up being needed later.
                if networkPopup == False:
                    networkPopup = True # Oh I'm toggling it!
                    keyInput = networkAddress # This is because we want to display the current broadcast address and have it be editable.
                    pygame.key.start_text_input()
                else: # This means we're closing the popup, so we must update the network with whatever address we ended on.
                    networkAddress = keyInput
                    if network.validate_network(networkAddress): # First checking validation, then changing network.
                        network.change_network(networkAddress)
                        print("Changed network to: " + networkAddress)
                    else:
                        print("Invalid network address.") # Very responsive and professional error handling comments if I say so myself.
                    networkPopup = False
                    pygame.key.stop_text_input()

            if typingCheck == False and networkPopup == False: # Conditional to lock the popup.
                #team switching
                if event.key == pygame.K_LEFT:
                    teamSelector = "red"
                if event.key == pygame.K_RIGHT:
                    teamSelector = "green"
                #move up a row
                if event.key == pygame.K_UP:
                    rowSelector -= 1
                #move down a row
                if event.key == pygame.K_DOWN:
                    rowSelector += 1
                #goes back to 14 if going up past 0
                if rowSelector < 0:
                    rowSelector = 14
                #goes back to 0 if going down past 14
                if rowSelector > 14:
                    rowSelector = 0

            #starts key input after pressing enter key
            if event.key == pygame.K_TAB and networkPopup == False: # Conditional to lock the popup.
                if typingCheck == False:
                    #starts editing for selected player
                    typingCheck = True
                    keyInput = ""
                    pygame.key.start_text_input()
                else:
                    if teamSelector == "red":
                        if inputMode == 0:
                            redTeam[rowSelector][0] = keyInput
                            inputMode = 1
                            keyInput = ""
                        elif inputMode == 1:
                            redTeam[rowSelector][1] = keyInput
                            inputMode = 0
                            typingCheck = False
                            keyInput = ""
                            pygame.key.stop_text_input()

                            #Inserts Red Team values into DB
                            curr.execute("INSERT INTO Players (id, codename) VALUES (%s, %s);", 
                                        (rowSelector + 1, redTeam[rowSelector][0]),
                                        )
                    if teamSelector == "green":
                        if inputMode == 0:
                            greenTeam[rowSelector][0] = keyInput
                            inputMode = 1
                            keyInput = ""
                        elif inputMode == 1:
                            greenTeam[rowSelector][1] = keyInput
                            inputMode = 0
                            typingCheck = False
                            keyInput = ""
                            pygame.key.stop_text_input()

                            #Inserts Green Team values into DB
                            curr.execute("INSERT INTO Players (id, codename) VALUES (%s, %s);", 
                                         (rowSelector + 16, greenTeam[rowSelector][0]),
                                         )

            #backspace to delete while typing
            if event.key == pygame.K_BACKSPACE:
                if networkPopup: # Popup doesn't care about the input mode.
                    keyInput = keyInput[:-1]
                elif typingCheck == True:
                    keyInput = keyInput[:-1]
                    
        #adds the typed key into the input (name/equipment ID)
        if event.type == pygame.TEXTINPUT:
            if networkPopup:
                keyInput += event.text
            elif typingCheck == True:
                if inputMode == 0:
                    keyInput += event.text
                elif inputMode == 1:
                    #makes sure that the user can only input numbers for equipment ID
                    if event.text.isdigit():
                        keyInput += event.text

        #if user closes entry window, stops the program
        if event.type == pygame.QUIT:
            gameRunning = False

    # Network Popup Drawing:
    if networkPopup:
        draw_popup(keyInput, "Enter Target Broadcast Address:") # Calls modular popup function with network parameters.

    #updates the screen
    pygame.display.flip()
    
# Actual Program Loop:
while gameRunning:
    if counter < 1500:
        #display Splash Screen
        counter += 1
        gameScreen.blit(logo, (0, 0)) # Adjusted to top left corner to fit logo across entire screen.
        pygame.display.flip()
    else:
        entryScreen()

# Closing Statements:
curr.close()
conn.close()
pygame.quit()
sys.exit()