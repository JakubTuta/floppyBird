import pygame
import os
import time
from random import randint
from math import sin

FPS = 60
WIDTH, HEIGHT = 450, 700
PRZERWA = 300
SCORE = 0
WHITE = (255, 255, 255)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLOPPY BIRD")

pygame.init()
fontPoints = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 80)
fontText = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 35)
fontTextBiggest = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 70)

class Bg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__background = pygame.Surface.convert(pygame.transform.scale(pygame.image.load(os.path.join("assets/background.png")), (WIDTH * 3, HEIGHT)))
    
    def draw(self):
        WIN.blit(self.__background, (self.x, self.y))
    
    def moveLeft(self):
        self.x -= 1
    
    def checkIfOutOfScreen(self):
        return self.x <= -WIDTH * 2
    
    def restart(self):
        self.x = 0


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__timeOfJump = 0
        self.__speed = 0
        self.__floppyBird = pygame.Surface.convert_alpha(pygame.transform.scale(pygame.image.load(os.path.join("assets/floppy_bird.png")), (80, 60)))
        self.__floppyBird_goingup = pygame.Surface.convert_alpha(pygame.transform.rotate(self.__floppyBird, 30))
        self.__floppyBird_goingdown = pygame.Surface.convert_alpha(pygame.transform.rotate(self.__floppyBird, -45))
        self.mask = pygame.mask.from_surface(self.__floppyBird)
        
    def draw(self):
        if self.__speed > 0:
            self.__floppyBird = self.__floppyBird_goingdown
        elif self.__speed < 0:
            self.__floppyBird = self.__floppyBird_goingup
        
        self.mask = pygame.mask.from_surface(self.__floppyBird)
        WIN.blit(self.__floppyBird, (self.x, self.y))
        
    def move(self):
        zwrocone = self.__checkIfJumpedGood()
        
        # w góre
        if zwrocone == 0:
            self.__speed = -10 + 50 * abs(self.__timeOfJump - time.time())
        # na szczycie
        elif zwrocone == 1:
            self.__timeOfJump = time.time()
        # w dół
        elif zwrocone == 2:
            self.__speed = 10 + 10 * abs(self.__timeOfJump - time.time())
        
        self.y += self.__speed
    
    def jump(self):
        self.__timeOfJump = time.time()
    
    def __checkIfJumpedGood(self):
        if time.time() - self.__timeOfJump < .15:
            return 0
        elif time.time() - self.__timeOfJump == .15:
            return 1
        else:
            return 2
    
    def getHeight(self):
        return self.__floppyBird.get_height()
    
    def getMidPoint(self):
        return self.x + self.__floppyBird.get_width() / 2


class Pipe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__pipe_up = pygame.Surface.convert_alpha(pygame.transform.scale(pygame.image.load(os.path.join("assets/pipe.png")), (75, HEIGHT * .6))) 
        self.__pipe_down = pygame.Surface.convert_alpha(pygame.transform.flip(self.__pipe_up, False, True))
        self.y2 = y - PRZERWA - self.__pipe_down.get_height()
        self.mask = pygame.mask.from_surface(self.__pipe_up)
        self.mask2 = pygame.mask.from_surface(self.__pipe_down)
    
    def draw(self):
        WIN.blit(self.__pipe_up, (self.x, self.y))
        WIN.blit(self.__pipe_down, (self.x, self.y - PRZERWA - self.__pipe_down.get_height()))
    
    def getMidPoint(self):
        return self.x + self.__pipe_up.get_width() / 2
    
    def checkIfOutOfScreen(self):
        return self.x + self.__pipe_up.get_width() < 0
    
    def restart(self, y):
        self.x = WIDTH
        self.y = y
        self.y2 = y - PRZERWA - self.__pipe_down.get_height()
    
    def moveLeft(self):
        self.x -= 4


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def collide2(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y2 - obj1.y
    return obj1.mask.overlap(obj2.mask2, (offset_x, offset_y)) != None


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
            pipe.restart(randint(PRZERWA + 100, HEIGHT - 100))
    
    if bird.y + bird.getHeight() < 0:
        return 1
    elif bird.y > HEIGHT:
        return 1


def check_collisions(bird, pipes):
    for pipe in pipes:
        if collide(bird, pipe) or collide2(bird, pipe):
            return 1


def check_points(bird, pipes):
    for pipe in pipes: 
        if abs(bird.getMidPoint() - pipe.getMidPoint()) < 3:
            global SCORE
            SCORE += 1


def print_points():
    textWidth = fontPoints.size(f'{SCORE}')[0]
    WIN.blit(fontPoints.render(f'{SCORE}', True, WHITE), (WIDTH / 2 - textWidth / 2, 10))


def gameover_screen(bg, bird, pipes):
    draw(bg, bird, pipes)
    print_points()
    
    textY = HEIGHT // 4
    text1 = fontTextBiggest.render(f"You  lost!", True, WHITE)
    text1Width, text1Height = fontTextBiggest.size(f"You  lost!")
    text2 = fontText.render(f"Press  any  key  to  continue", True, WHITE)
    text2Width = fontText.size(f"Press  any  key  to  continue")[0]
    
    WIN.blit(text1, (WIDTH / 2 - text1Width / 2, textY))
    WIN.blit(text2, (WIDTH / 2 - text2Width / 2, textY + text1Height + 20))
    
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    
    bg = Bg(0, 0)
    bird = Bird(WIDTH / 4, HEIGHT / 2)
    
    wartoscSin = 0
    textY = HEIGHT / 4
    loadingScreen = True
    
    while loadingScreen:
        clock.tick(FPS)
        
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
        
        text1 = fontText.render(f"Welcome  to  flappy  bird!", True, WHITE)
        text1Width, text1Height = fontText.size(f"Welcome  to  flappy  bird!")
        text2 = fontText.render(f"Press  space  to  start", True, WHITE)
        text2Width = fontText.size(f"Press  space  to  start")[0]
        
        WIN.blit(text1, (WIDTH / 2 - text1Width / 2, textY))
        WIN.blit(text2, (WIDTH / 2 - text2Width / 2, textY + text1Height + 20))
        
        pygame.display.update()
    
    pipes = []
    for i in range(2):
        pipes.append(Pipe(WIDTH + i * (WIDTH / 2 + 50), randint(PRZERWA + 100, HEIGHT - 100)))
    
    gameRunning = True
    while gameRunning:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.jump()
        
        move(bg, bird, pipes)
        check_points(bird, pipes)
        draw(bg, bird, pipes)
        print_points()
        pygame.display.update()
        if checkIfOutOfScreen(bg, bird, pipes) == 1 or check_collisions(bird, pipes) == 1:
            while True:
                gameover_screen(bg, bird, pipes)
                global SCORE
                SCORE = 0
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYUP:
                    main()


if __name__ == "__main__":
    main()
    pygame.quit()