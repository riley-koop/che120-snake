# Wormy, by Al Sweigart al@inventwithpython.com
# (Pygame) Lead the green snake around the screen eating red apples.

# Christopher van der Walt (21011000): CW
# Riley Koop (21013070): RK
# Matthieu Lavallee (21035855): ML

import random, pygame, sys              #CW: The modules random, pygame, and sys are imported into the file namespace
from pygame.locals import *             #CW: All the contents of the modulepygames.local are imported into the namespace

FPS = 15                                #CW: The value of 15 is assigned to the variable name of FPS.
WINDOWWIDTH = 840                       #CW: The value of 840 is assigned to the varible name WINDOWWIDTH.
WINDOWHEIGHT = 680                      #CW: The value of 840 is assigned to the varible name WINDOWHEIGHT.
CELLSIZE = 20                           #CW: The value of 20 is assigned to the varible name CELLSIZE.
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."             #CW: To ensure the window width is a multiple of the cell size, the remainder of the width divided by the cell size must be 0. By using assert, as long as the statement is true, the function will run. However, if the statement is false, then the program will raise an error. The value must be a multiple in order for the display to work properly. 
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."           #CW: The same steps are followed as above. However, this ensures that the height is a multiple of the cell size, ensuring that the display works properly.
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)                 #CW: To calculate the correct width of each cell, the width is divided by the cell size. In order to provide an integer output, the float output is converted to an integer. The result is assigned to the variable name CELLWIDTH.
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)               #CW: The same procedure is carried out as above, however, the height is calculated and assigned to CELLHEIGHT.

#             R    G    B
WHITE     = (255, 255, 255)             #CW: The colours are represented as a numerical input of their red, green, and blue intesities, and are assigned to descriptive variable names. So, when a colour is called later within the code, the element will adopt the necessary colours based on pixel intensity of the display
BLACK     = (  0,   0,   0)             #CW: The same occurs for the following, however with varying numerical values based on different colours
RED       = (255,   0,   0)             
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK                         #CW: Here, the data from the memory assigned to the desired colour is called and assigned to the variable name BGCOlOR so that it can be easily changed in one step if need be. The variable BGCOLOR will represent the backgroung colour of the interface 

UP = 'up'               #CW: The "up" key is called and reassigned to the variable name of "UP". Thus, the following programming can be more easily completed without the need to call the key "up" each time it is required.
DOWN = 'down'           #CW: The same occurs for the following key inputs.
LEFT = 'left'
RIGHT = 'right'

HEAD = 0            #CW: The worm's head is represented by the position of 0. This is what is known as syntactic sugar, a way to make the code more user-friendly and intuituve.

def main():         #CW: A new function, named main is being defined. The inputs of main are optional. 
    global FPSCLOCK, DISPLAYSURF, BASICFONT             #CW: Several variables are about to be defined. However, to ensure that they can be accessed throughout the code, not only in the namespace of the function, they are listed as global variables

    pygame.init()                                       #CW: A constructor is being called for a new class of objects. This means that, whenever an object in this class is created, several variables will be automatically assigned to it. For this, a predefined function from the module "pygame" is being used.
    FPSCLOCK = pygame.time.Clock()                      #CW: Here, the time is being called to the code with the pre-defined function from the "pygame" module and assigned to the variable FPSCLOCK. This will give the display a basis to work on to know when an element should move. Each instance of movement is referred to as a frame. Thus, the number of frames per second is equivalent to the number of changes within a given timeframe.
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))              #CW: The cooridnates of the display of the game is being defined. The variables of WINDOWWIDTH and WINDOWHEIGHT, defined above, are being called as the variables within the coordinates of the function, defined in the "pygame" module.
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)                #CW: The font to be displayed is being defined by a function defined in the "pygame" module. This is them assigned to the variable name of BASICFONT
    pygame.display.set_caption('Wormy')                 #CW: A pre-defined function from the "pygame" module is again being used to define the words displayed on the start screen of the game.

    showStartScreen()               #CW: A built-in function is called to ensure that a start screen is displayed when the game is opened.
    while True:                     #CW: While the if statements created below are satisfied, or are true, the code will do the following.
        runGame()                   #CW: A built-in function is used to keep the game running.
        showGameOverScreen()                #CW: Once the criteria to keep the game running are no longer met, the built-in function will display a "game over" screen


def runGame():      #RK: A new function named 'runGame' is being defined. There are no required inputs associated with this function.
    startx = random.randint(5, CELLWIDTH - 6)       #RK: at the beginning of the game, the start position of the worm on the x-axis is made to be a random position on the board.
                                                    #RK: Forcing the random value to be within 5 and CELLWIDTH-6 ensures the worm will be placed within the playing area.
    starty = random.randint(5, CELLHEIGHT - 6)      #RK: The start position of the worm on the y-axis is made to be a random position on the board.
                                                    #RK: Forcing the random value to be within 5 and CELLHEIGHT-6 ensures the worm will be placed within the playing area.
    wormCoords = [{'x': startx,     'y': starty},   #RK: At the beginning of the game, the worm is three pieces long, an array is created to handle worm coordinates, and three block coordinates are placed in it, creating the snake.
                  {'x': startx - 1, 'y': starty},   
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT       #RK: At the start of the game, the worm's direction will be to the right.

   
    apple = getRandomLocation() #RK: The first apple is created, and its coordinates are assigned randomly somewhere on the map

    while True: # RK: This is the main loop that continuously repeats the code necessary for the game to run properly.  
        for event in pygame.event.get():    #RK: This loop goes through the different events in the 'queue' of the pygame 'event' library.
            if event.type == QUIT:          #RK: If the event is of value 'QUIT', run the terminate() function to end the game. 
                terminate()
            elif event.type == KEYDOWN:     #RK: An if statement to check if a key has been pressed.
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:    #RK: If the left arrow key or the "A" key is pressed and the snake is not moving in the right direction, change the direction of movement to the left.
                    direction = LEFT                                                    #RK: This prevents a snake moving right from turning back on itself and killing itself.
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:  #RK: If the right arrow key or the "D" key is pressed and the snake is not moving in the left direction, change the direction of movement to the right.
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:     #RK: If the up arrow key or the "W" key is pressed and the snake is not moving in the down direction, change the direction of movement to up.
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:     #RK: If the down arrow key or the "S" key is pressed and the snake is not moving in the up direction, change the direction of movement to down.
                    direction = DOWN
                elif event.key == K_ESCAPE: #RK: If the escape key is pressed, the terminate function is called to end the game.
                    terminate()

        
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return             #RK: Check to see if the head of the worm has hit any of the four edges of the map. If the snake is off the map, end the game.
        for wormBody in wormCoords[1:]:    #RK: A loop to check the coordinates of each piece of the snake body except for the head.
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return         #RK: Check to see if the head of the worm has hit any of the body blocks of the snake. If it has, end the game.

        
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']: #RK: Check to see if the head of the worm has hit an apple and is "eating" it.
            apple = getRandomLocation()     #RK: Change the position of the apple to another random map location.
                                            #RK: Note that the tail segment is not being removed. Skipping this step for one iteration of the loop adds creates the illusion that the worm has gained another 'body piece'
        else:
            del wormCoords[-1]              #RK: Remove the end of the snake from the wormCoords array, to create the illusion that the snake is moving.

                                            #RK: The following lines add a new segment to the front of the snake. When the snake adds a piece in the front and loses one at the end, the snake looks to be moving across the screen, while maintaining its size.
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1} #RK: If the snake is moving in the up direction, create a new head at the current x position, and one y position less than the current one, because the y-values start at zero at the top of the screen, and increase moving down the screen.
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1} #RK: If the snake is moving in the down direction, create a new head at the current x position, and one y position greater than the current one
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']} #RK: If the snake is moving in the left direction, create a new head at one less than the current x position, and the current y position.
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']} #RK: If the snake is moving in the right direction, create a new head at one greater than the current x position, and the current y position.
        wormCoords.insert(0, newHead)       #RK: Insert the 'newHead' coordinate at the beginning of the 'wormCoords' array. This makes it the head of the snake.
        DISPLAYSURF.fill(BGCOLOR)           #RK: Make the background or 'display surface', solid black
        drawGrid()                          #RK: Use the drawgrid() function to draw the grid on the screen
        drawWorm(wormCoords)                #RK: Use the drawWorm() function to draw the worm on the screen by inputting the current worm coordinates to be drawm.
        drawApple(apple)                    #RK: Draw the apple by inputting the apple coordinates into the drawApple() function.
        drawScore(len(wormCoords) - 3)      #RK: Update the score based on the snake length. Since the default start length is 3, only increase the score for each length greater than 3.
        pygame.display.update()             #RK: Use the built in function to update the game display.
        FPSCLOCK.tick(FPS)                  #RK: Increase the frame rate of the game by 25 FPS i.e. update the framerate

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY) #RK: Create a message, and define its properties
    pressKeyRect = pressKeySurf.get_rect()                                  #RK: Create a rectangle to contain the message    
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)           #RK: Place the message at the given coordinates
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)                            #RK: Display the message


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()                         #RK: If there are any quit messages in the queue, run the terminate() function to end the game

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:               #RK: If no key is pressed on the start screen, do nothing
        return None
    if keyUpEvents[0].key == K_ESCAPE:      #RK: If escape key is pressed, end the game and close the window
        terminate()
    return keyUpEvents[0].key               #RK: return that the escape key was pressed


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)               #RK: Define the font and size to be used for the title
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)     #RK: Create one of the wormy titles to move around the screen
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)                #RK: Create the other wormy title to move around the screen

    degrees1 = 0  #RK: Initial rotation angle of both titles. Start at 0 degrees
    degrees2 = 0
    while True:   #RK: Start screen loop to check all parameters continuously
        DISPLAYSURF.fill(BGCOLOR)  #RK: Display the background colour
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1) #RK: Use the pygame built in function to rotate the first title by specified number of degrees
        rotatedRect1 = rotatedSurf1.get_rect()                       #RK: Create a rectangle to make the title an 'image'
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)    #RK: Make the center of the image the middle of the screen (the point to rotate around)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)                 #RK: Display the slightly rotated title.

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()                       #Repeat the above steps for the second title
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress(): #RK: Run the function, and if it returns a value, run the following code.
            pygame.event.get() #RK: Clear the event queue, as the event has been dealt with
            return
        pygame.display.update() #RK: Update the pygame display
        FPSCLOCK.tick(FPS) #RK: Update the framerate
        degrees1 += 3 #RK: Rotate by 3 degrees each frame
        degrees2 += 7 #RK: Rotate by 7 degrees each frame


def terminate():  #RK: A function to be called when wanting to end the game
    pygame.quit() #RK: Run the built in pygame quit function
    sys.exit()    #RK: Run the built in sys exit function
                #RK: The game is terminated and the window is closed.


#ML This function generates a random location within the cell.
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


#ML This function shows the Game Over screen when activated
def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150) #ML defines the font and size
    gameSurf = gameOverFont.render('Game', True, WHITE) #ML defines the font and size for the word 'Game'
    overSurf = gameOverFont.render('Over', True, WHITE) #ML defines the font and size for the word 'Over'
    gameRect = gameSurf.get_rect() #ML Returns a rectangle with the word "Game"
    overRect = overSurf.get_rect() #ML Returns a rectangle with the word "Over"
    gameRect.midtop = (WINDOWWIDTH / 2, 10) #ML Defines the height and width of the rectangle for "Game"
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25) #ML Defines the height and width of the rectangle for "Over"

    DISPLAYSURF.blit(gameSurf, gameRect) #ML Displays "Game" on the screen
    DISPLAYSURF.blit(overSurf, overRect) #ML Displays "Over" on the screen 
    drawPressKeyMsg() #ML Displays "Press a key to play."
    pygame.display.update() 
    pygame.time.wait(500) 
    checkForKeyPress() #ML Clears out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

#Ml This function displays the score
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE) #ML Sets the font and color of the score display
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10) #ML Sets the location of the score display (top left corner)
    DISPLAYSURF.blit(scoreSurf, scoreRect) #Displays the score

#ML This function draws the worm
def drawWorm(wormCoords):
    for coord in wormCoords: #ML When the worm is in the game area,
        x = coord['x'] * CELLSIZE #ML the length of the worm must be the cellsize
        y = coord['y'] * CELLSIZE #ML the height of the worm must be the cellsize
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) #ML defines the size of the outer part of the worm
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect) #ML draws the outer part of the worm (defines colour)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8) #ML defines the size of the inner part of the worm (slightly small than the outter part)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect) #ML draws the inner part of the worm (defines colour)


def drawApple(coord): #ML This function draws an apple
    x = coord['x'] * CELLSIZE #ML the length of the apple must be the cellsize
    y = coord['y'] * CELLSIZE #ML the height of the apple must be the cellsize
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE) #ML defines the size of the apple 
    pygame.draw.rect(DISPLAYSURF, RED, appleRect) #ML draws the apple (defines colour)


def drawGrid(): #ML This function draws the grid 
    for x in range(0, WINDOWWIDTH, CELLSIZE): #ML defines the vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT)) #ML draws the vertical lines
    for y in range(0, WINDOWHEIGHT, CELLSIZE): #ML defines the horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y)) #ML draws the horizontal lines


if __name__ == '__main__': #ML activates the code if the script is imported 
    main()