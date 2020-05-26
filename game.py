import pygame
import sys
from time import sleep

# BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640
# 이미지를 그냥 ./resource/background.png로 해도 되었는데 또 이상하게 안되서
# 그냥 전체리소스 경로를 지정해 놓음
resourcePath = '/home/donghyuk/바탕화면/Python/PyShooting/resource/'


def drawObject(obj, x, y):  # 배경화면 그리는 drawObject 함수
    global gamePad
    gamePad.blit(obj, (x, y))


def initGame():
    global gamePad, clock, background, fighter
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load(resourcePath+'background.png')
    fighter = pygame.image.load(resourcePath+'fighter.png')
    clock = pygame.time.Clock()


def runGame():
    global gamePad, clock, background, fighter

    fighterSize = fighter.get_rect().size  # 전투기 사이즈
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45  # 전투기 초기 위치
    y = padHeight * 0.9
    fighterX = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

        # gamePad.fill(BLACK)
        drawObject(background, 0, 0)

        drawObject(fighter, x, y)  # 전투기 표시

        pygame.display.update()

        clock.tick(60)
    pygame.quit()


initGame()
runGame()
