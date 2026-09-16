import pygame
import sys
import psycopg

try:
    with psycopg.connect(
        dbname="photon"
    ) as conn:
        pass
except Exception as e:
    print(f"An error occurred: {e}")

pygame.init()

#entry screen window size variables
windowWidth = 1000
windowHeight = 750

#entry screen window using the window size variable
gameScreen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Entry Terminal")

#Splash screen 
logo = pygame.image.load("photon-main\logo.jpg")
logo = pygame.transform.scale(logo, (800, 400))


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

def entryScreen():
    global gameRunning, rowSelector, teamSelector, typingCheck, keyInput, inputMode, redTeam, greenTeam

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
                
            if typingCheck == False:
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
            if event.key == pygame.K_RETURN:
                if typingCheck == False:
                    #starts editing for selected player
                    typingCheck = True
                    keyInput = ""
                    pygame.key.start_text_input()
            #moves to the next field after pressting tab
            if event.key == pygame.K_TAB:
                if typingCheck == True:
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

            #backspace to delete while typing
            if event.key == pygame.K_BACKSPACE:
                if typingCheck == True:
                    keyInput = keyInput[:-1]
                    
        #adds the typed key into the input (name/equipment ID)
        if event.type == pygame.TEXTINPUT:
            if typingCheck == True:
                if inputMode == 0:
                    keyInput += event.text
                elif inputMode == 1:
                    #makes sure that the user can only input numbers for equipment ID
                    if event.text.isdigit():
                        keyInput += event.text

        #if user closes entry window, stops the program
        if event.type == pygame.QUIT:
            gameRunning = False
    #updates the screen
    pygame.display.flip()
    

while gameRunning:
    if counter < 1500:
        #display Spash Screen
        counter += 1
        gameScreen.blit(logo, (125, 125))
        pygame.display.flip()
    else:
        entryScreen()
        
pygame.quit()
sys.exit()
