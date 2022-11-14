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

# Riley starts commenting here--------------------------------------------------------------------------------
def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


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


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()