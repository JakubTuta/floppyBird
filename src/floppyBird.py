import pygame
from random import randint
from math import sin
import json
from BackGround import Bg
from Pipe import Pipe
from Bird import Bird


SCORE = 0
WHITE = (255, 255, 255)


def loadSettings():
    with open("settings.json") as file:
        settings = json.load(file)
    return settings


def collide(bird, pipe):
    offset_x = pipe.x - bird.x
    offset_y = pipe.bottomY - bird.y
    return bird.mask.overlap(pipe.mask, (offset_x, offset_y)) != None


def collide2(bird, pipe):
    offset_x = pipe.x - bird.x
    offset_y = pipe.topY - bird.y
    return bird.mask.overlap(pipe.mask2, (offset_x, offset_y)) != None


def draw(bg, bird, pipes):
    bg.draw()
    bird.draw()
    for pipe in pipes:
        pipe.draw()


def move(bg, bird, pipes):
    bg.moveLeft()
    bird.move()
    for pipe in pipes:
        pipe.moveLeft()


def checkIfOutOfScreen(settings, bg, bird, pipes):
    if bg.checkIfOutOfScreen():
        bg.restart()
        
    for pipe in pipes:
        if pipe.checkIfOutOfScreen():
            pipe.restart(randint(settings["PRZERWA"] + 100, settings["HEIGHT"] - 100))
    
    return bird.y + bird.getHeight() < 0 or bird.y > settings["HEIGHT"]


def checkCollisions(bird, pipes):
    for pipe in pipes:
        if collide(bird, pipe) or collide2(bird, pipe):
            return 1


def checkPoints(bird, pipes):
    for pipe in pipes: 
        if pipe.checkPoints(bird):
            pipe.hasScored = True
            global SCORE
            SCORE += 1


def printPoints(WIN, fontPoints, WIDTH):
    textWidth = fontPoints.size(f'{SCORE}')[0]
    WIN.blit(fontPoints.render(f'{SCORE}', True, WHITE), (WIDTH / 2 - textWidth / 2, 10))


def gameoverScreen(WIN, settings, fonts, bg, bird, pipes):
    draw(bg, bird, pipes)
    printPoints(WIN, fonts["fontPoints"], settings["WIDTH"])
    
    textY = settings["HEIGHT"] // 4
    text1 = fonts["fontTextBiggest"].render("You  lost!", True, WHITE)
    text1Width, text1Height = fonts["fontTextBiggest"].size("You  lost!")
    
    text2 = fonts["fontText"].render("Press  any  key  to  continue", True, WHITE)
    text2Width = fonts["fontText"].size("Press  any  key  to  continue")[0]
    
    WIN.blit(text1, (settings["WIDTH"] / 2 - text1Width / 2, textY))
    WIN.blit(text2, (settings["WIDTH"] / 2 - text2Width / 2, textY + text1Height + 20))
    
    pygame.display.update()


def main():
    settings = loadSettings()
    
    WIN = pygame.display.set_mode((settings["WIDTH"], settings["HEIGHT"]))
    pygame.display.set_caption("FLOPPY BIRD")

    pygame.init()
    fonts = {
        "fontPoints": pygame.font.Font("fonts/ARCADECLASSIC.ttf", 80),
        "fontText": pygame.font.Font("fonts/ARCADECLASSIC.ttf", 35),
        "fontTextBiggest": pygame.font.Font("fonts/ARCADECLASSIC.ttf", 70)
    }
    
    bg = Bg(WIN, 0, 0)
    bird = Bird(WIN, settings["WIDTH"] / 4, settings["HEIGHT"] / 2)
    
    wartoscSin = 0
    textY = settings["HEIGHT"] / 4
    loadingScreen = True
    
    clock = pygame.time.Clock()
    while loadingScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        keyz = pygame.key.get_pressed()
        if keyz[pygame.K_SPACE]:
            loadingScreen = False
            bird.jump()
        
        bg.draw()
        bg.moveLeft()
        bird.draw()
        
        textY -= sin(wartoscSin)
        wartoscSin += .1
        
        text1 = fonts["fontText"].render(f"Welcome  to  flappy  bird!", True, WHITE)
        text1Width, text1Height = fonts["fontText"].size(f"Welcome  to  flappy  bird!")
        text2 = fonts["fontText"].render(f"Press  space  to  start", True, WHITE)
        text2Width = fonts["fontText"].size(f"Press  space  to  start")[0]
        
        WIN.blit(text1, (settings["WIDTH"] / 2 - text1Width / 2, textY))
        WIN.blit(text2, (settings["WIDTH"] / 2 - text2Width / 2, textY + text1Height + 20))
        
        pygame.display.update()
        clock.tick(settings["FPS"])
    
    pipes = []
    for i in range(2):
        pipes.append(Pipe(WIN, settings["WIDTH"] + i * (settings["WIDTH"] / 2 + 50), randint(settings["PRZERWA"] + 100, settings["HEIGHT"] - 100)))
    
    gameRunning = True
    spacePressed = False
    
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not spacePressed:
                    spacePressed = True
                    bird.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and spacePressed:
                    spacePressed = False
        
        move(bg, bird, pipes)
        checkPoints(bird, pipes)
        draw(bg, bird, pipes)
        printPoints(WIN, fonts["fontPoints"], settings["WIDTH"])
        pygame.display.update()
        
        if checkIfOutOfScreen(settings, bg, bird, pipes) == 1 or checkCollisions(bird, pipes) == 1:
            while True:
                gameoverScreen(WIN, settings, fonts, bg, bird, pipes)
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYUP:
                    global SCORE
                    SCORE = 0
                    main()
        
        clock.tick(settings["FPS"])


if __name__ == "__main__":
    main()
    pygame.quit()