import pygame
import json
import os

class Bg:
    settings = {}
    WIN = None
    
    def __init__(self, WIN, x, y):
        Bg.WIN = WIN
        with open("settings.json") as file:
            Bg.settings = json.load(file)
        
        self.x = x
        self.y = y
        self.__background = pygame.Surface.convert(pygame.transform.scale(pygame.image.load(os.path.join("assets/background.png")), (Bg.settings["WIDTH"] * 3, Bg.settings["HEIGHT"])))
    
    def draw(self):
        Bg.WIN.blit(self.__background, (self.x, self.y))
    
    def moveLeft(self):
        self.x -= 1
    
    def checkIfOutOfScreen(self):
        return self.x <= -Bg.settings["WIDTH"] * 2
    
    def restart(self):
        self.x = 0