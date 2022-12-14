#Created by: Riley Koop, Christopher van der Walt, and Matthieu Lavallee



import random, pygame, sys, time
from pygame.locals import *
numapples=15
numobstacles=15
remove=False
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
PURPLE    = (239,   0, 255)
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
    applesx=[]
    applesy=[]
    obstaclesx=[]
    obstaclesy=[]
    mover_coords=[0, random.randint(1, CELLHEIGHT-1), 0, random.randint(1, CELLHEIGHT-1), 0, random.randint(1, CELLHEIGHT-1)]
    moverUpdate= True
  
    

    i=0
    for i in range(numapples):
        applesx.insert(len(applesx),random.randint(1, CELLWIDTH-1))
        applesy.insert(len(applesy),random.randint(1, CELLHEIGHT-1))
        i+=1

    
    for i in range(numobstacles):
        obstaclesx.insert(len(applesx),random.randint(1, CELLWIDTH-1))
        obstaclesy.insert(len(applesy),random.randint(1, CELLHEIGHT-1))
        i+=1
    #apple = getRandomLocation()
    
    

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
        
            


        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over
        if counter == -1:
            pygame.time.set_timer(timer_event, 0)
            return

        # check if worm has eaten an apply
        for j in range(len(applesx)):
            if wormCoords[HEAD]['x'] != applesx[j] or wormCoords[HEAD]['y'] != applesy[j]:
            # don't remove worm's tail segment
            #apple = getRandomLocation() # set a new apple somewhere
                remove=True

            else:
                
                remove=False
                applesx[j]=-1
                applesy[j]=-1
                break

        i=0
        j=1
        while i<5:
            if wormCoords[HEAD]['x'] != mover_coords[i] or wormCoords[HEAD]['y'] != mover_coords[j]:
                j+=2
                i+=2
            else: return


      

        for i in range(len(obstaclesx)):
            if wormCoords[HEAD]['x'] != obstaclesx[i] or wormCoords[HEAD]['y'] != obstaclesy[i]:
                None
            else: return

        
                

       
        if remove==True:
            del wormCoords[-1] # remove worm's tail segment
            remove=False
           

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
        
        moverUpdate = True
        i=0
        j=1
        while i<5 and moverUpdate==True:
            if mover_coords[i]<=CELLWIDTH:
                
                x = mover_coords[i] * CELLSIZE
                y = mover_coords[j] * CELLSIZE
                
                moverRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
                pygame.draw.rect(DISPLAYSURF, PURPLE, moverRect)
                mover_coords[i]+=1
                
            if mover_coords[i]>=CELLWIDTH:
                mover_coords[i] = 0
                mover_coords[j] = random.randint(1, CELLHEIGHT-1)

            if i==4:
                moverUpdate=False

            
            j+=2
            i+=2
            

                

             
        drawWorm(wormCoords)
        i=0
        while i<numapples:
            drawApple(applesx[i], applesy[i])
            i+=1

        i=0
        while i<numobstacles:
            drawObstacle(obstaclesx[i], obstaclesy[i])
            i+=1
        drawScore(len(wormCoords) - 3)
        clock_rect = clock_text.get_rect(topleft = (10,10))
        DISPLAYSURF.blit(clock_text, clock_rect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 430, WINDOWHEIGHT - 40)
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
    scoreRect.topleft = (WINDOWWIDTH - 100, 10)
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
    if coord1!=-1 and coord2!=-1:
        x = coord1 * CELLSIZE
        y = coord2 * CELLSIZE
        appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawObstacle(coord1, coord2):
    if coord1!=-1 and coord2!=-1:
        x = coord1 * CELLSIZE
        y = coord2 * CELLSIZE
        obstacleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, YELLOW, obstacleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


   

   


if __name__ == '__main__':
    main()