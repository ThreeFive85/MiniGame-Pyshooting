import pygame
import sys
import random
from time import sleep

# BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640
# 이미지를 그냥 ./resource/background.png로 해도 되었는데 또 이상하게 안되서
# 그냥 전체리소스 경로를 지정해 놓음
resourcePath = '/home/donghyuk/바탕화면/Python/PyShooting/resource/'
rockImage = [resourcePath+'rock01.png', resourcePath+'rock02.png', resourcePath+'rock03.png', resourcePath+'rock04.png',
             resourcePath+'rock05.png', resourcePath+'rock06.png', resourcePath +
             'rock07.png', resourcePath+'rock08.png',
             resourcePath+'rock09.png', resourcePath+'rock10.png', resourcePath +
             'rock11.png', resourcePath+'rock12.png',
             resourcePath+'rock13.png', resourcePath+'rock14.png', resourcePath +
             'rock15.png', resourcePath+'rock16.png',
             resourcePath+'rock17.png', resourcePath+'rock18.png', resourcePath +
             'rock19.png', resourcePath+'rock20.png',
             resourcePath+'rock21.png', resourcePath+'rock22.png', resourcePath +
             'rock23.png', resourcePath+'rock24.png',
             resourcePath+'rock25.png', resourcePath+'rock26.png', resourcePath +
             'rock27.png', resourcePath+'rock28.png',
             resourcePath+'rock29.png', resourcePath+'rock30.png', ]
explosionSound = [resourcePath+'explosion01.wav', resourcePath+'explosion02.wav', resourcePath+'explosion03.wav',
                  resourcePath+'explosion04.wav']

# 운석을 맞춘 개수 계산


def writeScore(count):
    global gamePad
    font = pygame.font.Font(resourcePath+'NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))


def writePassed(count):
    global gamePad
    font = pygame.font.Font(resourcePath+'NanumGothic.ttf', 20)
    text = font.render('놓친 운석:' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))

# 게임 메서지 출력


def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font(resourcePath+'NanumGothic.ttf', 60)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()  # 배경 음악 정지
    gameOverSound.play()  # 게임 오버 사운드 재생
    sleep(5)  # 5초 쉬고 다시 시작
    pygame.mixer.music.play(-1)  # 배경 음악 재생
    runGame()

# 전투기가 운석과 충돌했을 때 메세지 출력


def crash():
    global gamePad
    writeMessage('전투기 파괴!!!')

# 게임 오버 메시지 보이기


def gameOver():
    global gamePad
    writeMessage('게임 오버!!!')


def drawObject(obj, x, y):  # 배경화면 그리는 drawObject 함수
    global gamePad
    gamePad.blit(obj, (x, y))


def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load(resourcePath+'background.png')
    fighter = pygame.image.load(resourcePath+'fighter.png')
    missile = pygame.image.load(resourcePath+'missile.png')
    explosion = pygame.image.load(resourcePath+'explosion.png')
    pygame.mixer.music.load(resourcePath+'music.wav')  # 배경음악
    pygame.mixer.music.play(-1)  # 배경음악 재생
    missileSound = pygame.mixer.Sound(resourcePath+'missile.wav')  # 미사일소리
    gameOverSound = pygame.mixer.Sound(resourcePath+'gameover.wav')  # 게임오버 사운드
    clock = pygame.time.Clock()


def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound

    fighterSize = fighter.get_rect().size  # 전투기 사이즈
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45  # 전투기 초기 위치
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(
        random.choice(explosionSound))  # 랜덤하게 폭발 사운드

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    # 미사일에 운석이 맞았을때
    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:  # 전투기 움직이기
                if event.key == pygame.K_LEFT:
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:
                    fighterX += 5

                elif event.key == pygame.K_SPACE:  # 스페이스바를 누르면 미사일 발사
                    missileSound.play()  # 스페이스를 누르면 미사일사운드 플레이
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:  # 왼쪽,오른쪽 키보드를 떘을때
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        # gamePad.fill(BLACK)
        drawObject(background, 0, 0)

        x += fighterX  # 키보드로부터 변경된 비행기 좌표 반영
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:  # 게임 화면에서 비행기가 오른쪽으로 끝까지 갔을 경우
            x = padWidth - fighterWidth

        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or \
                    (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()

        drawObject(fighter, x, y)  # 전투기 표시

        if len(missileXY) != 0:
            # enumerate로 missileXY에 대해 전체적으로 돌고
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10  # 미사일은 위로 발사되기깨문에 y좌표에서 -10씩
                missileXY[i][1] = bxy[1]  # 미사일은 여러개이기때문에 bxy에 대한 값을 넣어 준다.

                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:  # 미사일이 화면 밖으로 넘어 갔을때
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:  # 미사일 실제 그리기
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        # 운석 맞춘 점수 표시
        writeScore(shotCount)

        rockY += rockSpeed  # 운석이 아래로 움직임
        # 운석이 지구로 떨어진 경우
        if rockY > padHeight:
            # 새로운 운석을 만들어 준다
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        # 운석 3개를 놓치면 게임 오버
        if rockPassed == 3:
            gameOver()

        # 놓친 운석 수 표시
        writePassed(rockPassed)

        # 운석을 맞춘 경우
        if isShot:
            # 운석 폭발
            drawObject(explosion, rockX, rockY)  # 운석 폭발 그림
            destroySound.play()  # 운석 폭발 사운드 재생

            # 새로운 운석(랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            # 운석을 맞추면 속도 증가
            rockSpeed += 0.2
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)  # 운석 그리기

        pygame.display.update()

        clock.tick(60)
    pygame.quit()


initGame()
runGame()
