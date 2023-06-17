import pygame
import json
import os

class Pipe:
    settings = {}
    WIN = None
    
    def __init__(self, WIN, x, y):
        Pipe.WIN = WIN
        with open("settings.json") as file:
            Pipe.settings = json.load(file)
        
        self.x = x
        self.y = y
        self.__pipe_up = pygame.Surface.convert_alpha(pygame.transform.scale(pygame.image.load(os.path.join("assets/pipe.png")), (75, Pipe.settings["HEIGHT"] * .6))) 
        self.__pipe_down = pygame.Surface.convert_alpha(pygame.transform.flip(self.__pipe_up, False, True))
        self.y2 = y - Pipe.settings["PRZERWA"] - self.__pipe_down.get_height()
        self.mask = pygame.mask.from_surface(self.__pipe_up)
        self.mask2 = pygame.mask.from_surface(self.__pipe_down)
        self.hasScored = False
    
    def draw(self):
        Pipe.WIN.blit(self.__pipe_up, (self.x, self.y))
        Pipe.WIN.blit(self.__pipe_down, (self.x, self.y - Pipe.settings["PRZERWA"] - self.__pipe_down.get_height()))
    
    def getMidPoint(self):
        return self.x + self.__pipe_up.get_width() / 2
    
    def checkIfOutOfScreen(self):
        return self.x + self.__pipe_up.get_width() < 0
    
    def restart(self, y):
        self.x = Pipe.settings["WIDTH"]
        self.y = y
        self.y2 = y - Pipe.settings["PRZERWA"] - self.__pipe_down.get_height()
        self.hasScored = False
    
    def moveLeft(self):
        self.x -= 4
    
    def checkPoints(self, bird):
        return abs(bird.getMidPoint() - self.getMidPoint()) < 4 and not self.hasScored