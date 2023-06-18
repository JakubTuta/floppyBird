import pygame
import time

class Bird:
    WIN = None
    
    def __init__(self, WIN, x, y, graphics):
        Bird.WIN = WIN
        
        self.x = x
        self.y = y
        self.__timeOfJump = time.time()
        self.__speed = 0
        self.__floppyBird = graphics[0]
        self.__floppyBird_goingup = graphics[1]
        self.__floppyBird_goingdown = graphics[2]
        self.mask = pygame.mask.from_surface(self.__floppyBird)
        
    def draw(self):
        if self.__speed > 0:
            self.__floppyBird = self.__floppyBird_goingdown
        elif self.__speed < 0:
            self.__floppyBird = self.__floppyBird_goingup
        
        self.mask = pygame.mask.from_surface(self.__floppyBird)
        Bird.WIN.blit(self.__floppyBird, (self.x, self.y))
        
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
        if time.time() - self.__timeOfJump < .2:
            return 0
        elif time.time() - self.__timeOfJump == .2:
            return 1
        else:
            return 2
    
    def getHeight(self):
        return self.__floppyBird.get_height()
    
    def getWidth(self):
        return self.__floppyBird.get_width()
    
    def getMidPoint(self):
        return self.x + self.__floppyBird.get_width() / 2