import pygame
import json
import os
import random

class Pipe:
    with open("settings.json") as file:
        settings = json.load(file)
    WIN = None
    pipeGraphic = pygame.image.load(os.path.join("assets/pipe.png"))
    pipeGraphic.set_colorkey((255, 255, 255))
    
    def __init__(self, WIN, x, y):
        Pipe.WIN = WIN
        
        self.x = x
        self.bottomY = y
        self.__pipe_up = pygame.transform.scale(Pipe.pipeGraphic, (70, Pipe.settings["HEIGHT"] * .7)).convert_alpha()
        self.__pipe_down = pygame.transform.flip(self.__pipe_up, False, True)
        self.topY = y - Pipe.settings["PRZERWA_Y"] - self.__pipe_down.get_height()
        self.mask = pygame.mask.from_surface(self.__pipe_up)
        self.mask2 = pygame.mask.from_surface(self.__pipe_down)
        self.hasScored = False
    
    def draw(self):
        Pipe.WIN.blit(self.__pipe_up, (self.x, self.bottomY))
        Pipe.WIN.blit(self.__pipe_down, (self.x, self.bottomY - Pipe.settings["PRZERWA_Y"] - self.__pipe_down.get_height()))
    
    def getMidPoint(self):
        return self.x + self.__pipe_up.get_width() / 2
    
    def getWidth(self):
        return self.__pipe_up.get_width()
    
    def checkIfOutOfScreen(self):
        return self.x + self.__pipe_up.get_width() < 0
    
    def restart(self):
        self.x = Pipe.settings["WIDTH"]
        self.bottomY = random.randint(Pipe.settings["PRZERWA_Y"] + Pipe.settings["HEIGHT"] * .15, Pipe.settings["HEIGHT"] * .85)
        self.topY = self.bottomY - Pipe.settings["PRZERWA_Y"] - self.__pipe_down.get_height()
        self.hasScored = False
    
    def moveLeft(self):
        self.x -= 4
    
    def checkPoints(self, bird):
        return abs(bird.getMidPoint() - self.getMidPoint()) < 4 and not self.hasScored
    
    def getTopPipeY(self):
        return self.topY + self.__pipe_up.get_height()
    
    def getBottomPipeY(self):
        return self.bottomY