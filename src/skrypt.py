import os
try:
    import pygame
    import neat
except:
    os.system("pip install pygame --pre")
    os.system("pip install neat-python")
os.popen("python floppyBird.py")