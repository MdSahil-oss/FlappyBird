import pygame
import random
from pygame.locals import *
import sys

from pygame.time import Clock

# Global variable 
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'sprites/bird.png'
BACKGROUND = 'sprites/background.png'
PIPE = 'sprites/pipe.png'

def welcomeScreen():
    '''This is to display the welcome Screen which will show the user to start the Game'''
    playerX = int(SCREENWIDTH/5)
    # - GAME_SPRITES['player'].get_height()
    playerY = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messageX = int((SCREENWIDTH  - GAME_SPRITES["message"].get_width())/2)
    messageY = int(SCREENHEIGHT * 0.13)
    baseX = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                return 
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerX,playerY))
                SCREEN.blit(GAME_SPRITES['message'],(messageX,messageY))
                SCREEN.blit(GAME_SPRITES['base'],(baseX,GROUNDY))
                pygame.display.update()
                FPSCLOCK = pygame.time.Clock()
                FPSCLOCK.tick(FPS)

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

def mainGame():
    score = 0
    playerX = int(SCREENWIDTH/5)
    playerY = int(SCREENHEIGHT/2)
    baseX=0
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    
    upperPipe = [
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']},
    ]

    lowerPipe = [
        {"x":SCREENWIDTH+200,"y":newPipe1[1]['y']},
        {"x":SCREENWIDTH+200+(SCREENWIDTH/2),"y":newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8
    playerFlapped = False
    

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_SPACE):
                playerVelY = playerFlapAccv
                playerFlapped = True
                GAME_SOUNDS['wing'].play()
        crashTest = isCollide(playerX,playerY,upperPipe,lowerPipe)
        if crashTest:
            return 
        
        playerMidPos = playerX+(GAME_SPRITES['player'].get_width()/2)
        for pipe in upperPipe:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
        
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        
        if playerFlapped:
            playerFlapped=False
        playerHeight = GAME_SPRITES['player'].get_height()
        playerY = playerY + min(playerVelY, GROUNDY - playerY - playerHeight)
        
        for upperPipes,lowerPipes in zip(upperPipe,lowerPipe):
            upperPipes['x'] += pipeVelX
            lowerPipes['x'] += pipeVelX
        
        if upperPipe[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
            upperPipe.pop(0)
            lowerPipe.pop(0)

        if 0<upperPipe[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipe.append(newpipe[0])
            lowerPipe.append(newpipe[1])
        


        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipes,lowerPipes in zip(upperPipe,lowerPipe):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipes['x'],upperPipes['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipes['x'],lowerPipes['y']))
        SCREEN.blit(GAME_SPRITES['base'],(baseX,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerX,playerY))
        myDigits = [int(i) for i in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK = pygame.time.Clock()
        FPSCLOCK.tick(FPS)
def isCollide(playerX,playerY,upperPipe,lowerPipe):
    if playerY > GROUNDY-25 or playerY < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipe:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if playerY < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipe:
        if (playerY + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True   
    return False   
        
if __name__=="__main__":
    pygame.init()
    
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
        )
    GAME_SPRITES['message'] = pygame.image.load('sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('sprites/message.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate((pygame.image.load(PIPE).convert_alpha()),180),pygame.image.load(PIPE).convert_alpha())

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()


    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')

    while True:
        welcomeScreen()      # This is to display the Welcome Screen
        mainGame()           # This is to display the Main Screen