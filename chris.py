# Wormy, by Al Sweigart al@inventwithpython.com
# (Pygame) Lead the green snake around the screen eating red apples.


import numpy as np
import random, pygame, sys
from pygame.locals import *
num_Apples=15
FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

clock = pygame.time.Clock()
timer_interval = 1000
timer_event = pygame.USEREVENT + 1

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0, 127)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (255, 255,   0)
BLUE      = (  0, 230, 255)
ACOLOR = YELLOW
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('ocraextended', 18)
    pygame.display.set_caption('Wormy')
    pygame.time.set_timer(timer_event, timer_interval)

    showStartScreen()
    
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    counter = 30
    # Start the apple in a random place.
    #apple = getRandomLocation()
    
    applesx=[31,11,24,7,16,4,9,8,19,22,3,27,30,5,13]
    applesy=[8,19,22,3,27,30,5,13,5,11,24,7,16,4,9]
    #applesx = np.empty(num_Apples, dtype=int)
    #applesy = np.empty(num_Apples, dtype=int)
   
    #for i in range(num_Apples):
        #applesx.insert(len(applesx),randomx())
        #applesy.insert(len(applesy),randomy())
        #print(applesx)
        #print(CELLWIDTH)
        #applesx[i]=randomx()
        #applesy[i]=randomy()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == timer_event:
                counter -= 1
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
        clock_font = pygame.font.SysFont('ocraextended', 18)
        clock_text = clock_font.render('Time : ' + str(counter), True, WHITE)
        clock_Rect = clock_text.get_rect()
        clock_Rect.topleft = (10, 10)
        #DISPLAYSURF.blit(clock_text, clock_Rect)
        

        # check if the worm has hit itself or the edge
        #print(applesx[1])
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over
        if counter == -1:
            pygame.time.set_timer(timer_event, 0)
            return

        # check if worm has eaten an apply
        for i in range(len(applesx)):
            #print(applesx[i])
            #print(type(wormCoords[HEAD]['x']), type(applesx[0]))
            
            if wormCoords[HEAD]['x'] == applesx[i] and wormCoords[HEAD]['y'] == applesy[i]:
                print("HELLO")
                 #don't remove worm's tail segment
                #applesx[i]=-1
                #applesy[i]=-1
           # else:
                #del wormCoords[-1] # remove worm's tail segment

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
        drawWorm(wormCoords)
        for i in range(len(applesx)):
            if applesx[i]>=0 and applesy[i]>= 0:
                drawApple(applesx[i], applesy[i])
        #drawApple(apple)
        drawScore(len(wormCoords) - 3)
        clock_rect = clock_text.get_rect(topleft = (10,10))
        DISPLAYSURF.blit(clock_text, clock_rect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 430, WINDOWHEIGHT - 30)
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
    titleFont = pygame.font.SysFont('ocraextended', 100)
    titleSurf1 = titleFont.render('Wormy!', True, YELLOW, RED)
    titleSurf2 = titleFont.render('Wormy!', True, BLUE)

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


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def randomx():
    return random.randint(5, CELLWIDTH - 6)

def randomy():
    return random.randint(5, CELLHEIGHT - 6)


def showGameOverScreen():
    gameOverFont = pygame.font.SysFont('ocraextended', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)




def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord1, coord2):
    x = coord1 
    y = coord1 
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, ACOLOR, appleRect)


#def drawGrid():
    #for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        #pygame.draw.line(DISPLAYSURF, WHITE, (x, 0), (x, WINDOWHEIGHT))
    #for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        #pygame.draw.line(DISPLAYSURF, WHITE, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()