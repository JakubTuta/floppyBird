import pygame
from random import randint
from math import sin
import json
from BackGround import Bg
from Pipe import Pipe
from Bird import Bird


SCORE = 0
WHITE = (255, 255, 255)

with open("settings.json") as file:
    settings = json.load(file)

WIN = pygame.display.set_mode((settings["WIDTH"], settings["HEIGHT"]))
pygame.display.set_caption("FLOPPY BIRD")
clock = pygame.time.Clock()

pygame.init()
fonts = {
    "fontPoints": pygame.font.Font("fonts/ARCADECLASSIC.ttf", 90),
    "fontText": pygame.font.Font("fonts/ARCADECLASSIC.ttf", 35),
    "fontTextBiggest": pygame.font.Font("fonts/ARCADECLASSIC.ttf", 70)
}


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


def checkIfOutOfScreen(bg, bird, pipes):
    if bg.checkIfOutOfScreen():
        bg.restart()
    
    for pipe in pipes:
        if pipe.checkIfOutOfScreen():
            pipe.restart()
    
    return bird.y + bird.getHeight() < 0 or bird.y > settings["HEIGHT"]


def checkCollisions(bird, pipes):
    for pipe in pipes:
        if collide(bird, pipe) or collide2(bird, pipe):
            return True
    return False


def checkPoints(bird, pipes):
    for pipe in pipes: 
        if pipe.checkPoints(bird):
            pipe.hasScored = True
            global SCORE
            SCORE += 1


def printPoints():
    textWidth = fonts["fontPoints"].size(f'{SCORE}')[0]
    WIN.blit(fonts["fontPoints"].render(f'{SCORE}', True, WHITE), (settings["WIDTH"] / 2 - textWidth / 2, 10))


def gameoverScreen(bg, bird, pipes):
    draw(bg, bird, pipes)
    printPoints()
    
    textY = settings["HEIGHT"] // 4
    text1 = fonts["fontTextBiggest"].render("You  lost!", True, WHITE)
    text1Width, text1Height = fonts["fontTextBiggest"].size("You  lost!")
    
    text2 = fonts["fontText"].render("Press  any  key  to  continue", True, WHITE)
    text2Width = fonts["fontText"].size("Press  any  key  to  continue")[0]
    
    WIN.blit(text1, (settings["WIDTH"] / 2 - text1Width / 2, textY))
    WIN.blit(text2, (settings["WIDTH"] / 2 - text2Width / 2, textY + text1Height + 20))
    
    pygame.display.update()


def main():
    bg = Bg(WIN, 0, 0)
    bird = Bird(WIN, settings["WIDTH"] / 4, settings["HEIGHT"] / 2)
    
    wartoscSin = 0
    textY = settings["HEIGHT"] / 4
    loadingScreen = True
    
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
        wartoscSin += .05
        
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
        pipes.append(Pipe(WIN, settings["WIDTH"] + settings["PRZERWA_X"] * i, randint(settings["PRZERWA_Y"] + settings["HEIGHT"] * .15, settings["HEIGHT"] * .85)))
    
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
        draw(bg, bird, pipes)
        checkPoints(bird, pipes)
        printPoints()
        
        if checkIfOutOfScreen(bg, bird, pipes) or checkCollisions(bird, pipes):
            while True:
                gameoverScreen(bg, bird, pipes)
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYUP:
                    global SCORE
                    SCORE = 0
                    main()
        
        pygame.display.update()
        clock.tick(settings["FPS"])


if __name__ == "__main__":
    main()
    pygame.quit()