import pygame                           # pip install pygame / pip install pygame --pre
import neat                             # pip install neat-python
from random import randint
import json
import os
from BackGround import Bg
from Pipe import Pipe
from Bird import Bird

WHITE = (255, 255, 255)
RED = (255, 0, 0)
SCORE = 0
GEN = 0

with open("settings.json") as file:
    settings = json.load(file)

WIN = pygame.display.set_mode((settings["WIDTH"], settings["HEIGHT"]))
pygame.display.set_caption("FLOPPY BIRD")

clock = pygame.time.Clock()

pygame.init()
font = pygame.font.SysFont(None, 40)

baseBirdGraphic = pygame.transform.scale(pygame.image.load(os.path.join("assets/floppy_bird.png")), (50, 30)).convert_alpha()
birdGraphics = [baseBirdGraphic,
                pygame.transform.rotate(baseBirdGraphic, 30),
                pygame.transform.rotate(baseBirdGraphic, -45)]


def collide(bird, pipe):
    offset_x = pipe.x - bird.x
    offset_y = pipe.bottomY - bird.y
    return bird.mask.overlap(pipe.mask, (offset_x, offset_y)) != None


def collide2(bird, pipe):
    offset_x = pipe.x - bird.x
    offset_y = pipe.topY - bird.y
    return bird.mask.overlap(pipe.mask2, (offset_x, offset_y)) != None


def draw(bg, birds, pipes):
    bg.draw()
    
    for bird in birds:
        bird.draw()
    
    for pipe in pipes:
        pipe.draw()


def move(bg, pipes):
    bg.moveLeft()
    for pipe in pipes:
        pipe.moveLeft()


def checkIfOutOfScreen(settings, bg, bird, pipes):
    if bg.checkIfOutOfScreen():
        bg.restart()
    
    for i, pipe in enumerate(pipes):
        if pipe.checkIfOutOfScreen():
            pipe.restart()
            pipes.pop(i)
            pipes.append(pipe)
    
    return bird.y + bird.getHeight() < 0 or bird.y > settings["HEIGHT"]


def checkPoints(bird, pipes):
    for pipe in pipes: 
        if pipe.checkPoints(bird):
            pipe.hasScored = True
            return True
    return False


def checkCollisions(bird, pipes):
    for pipe in pipes:
        if collide(bird, pipe) or collide2(bird, pipe):
            return True
    return False


def drawLine(WIN, bird, pipe):
    pygame.draw.line(WIN, RED, (bird.x + (bird.getWidth() / 2), bird.y + (bird.getHeight() / 2)), (pipe.x + (pipe.getWidth() / 2), pipe.getTopPipeY()), width=5)
    pygame.draw.line(WIN, RED, (bird.x + (bird.getWidth() / 2), bird.y + (bird.getHeight() / 2)), (pipe.x + (pipe.getWidth() / 2), pipe.getBottomPipeY()), width=5)


def printText(WIN, birdsAlive):
    textWidth = font.size(f"Score: {SCORE}")[0]
    WIN.blit(font.render(f"Score: {SCORE}", True, WHITE), (settings["WIDTH"] - textWidth - 10, 10))
    
    textHeight = font.size(f"Generation: {GEN}")[1]
    WIN.blit(font.render(f"Generation: {GEN}", True, WHITE), (10, 10))
    WIN.blit(font.render(f"Birds: {birdsAlive}", True, WHITE), (10, 10 + textHeight + 10))


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    population.run(main, 50)


def main(genomes, config):
    global GEN
    GEN += 1
    
    bg = Bg(WIN, 0, 0)
    
    nets = []
    ge = []
    birds = []
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)
        birds.append(Bird(WIN, settings["WIDTH"] / 4, settings["HEIGHT"] / 2, birdGraphics))
    
    pipes = []
    for i in range(2):
        pipes.append(Pipe(WIN, settings["WIDTH"] + settings["PRZERWA_X"] * i, randint(settings["PRZERWA_Y"] + settings["HEIGHT"] * .15, settings["HEIGHT"] * .85)))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        if len(birds) == 0:
            global SCORE
            SCORE = 0
            break
        
        move(bg, pipes)
        draw(bg, birds, pipes)
        printText(WIN, len(birds))
        
        pipeIndex = 0
        if birds[0].x > pipes[0].x + pipes[0].getWidth():
            pipeIndex = 1
        
        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += .1
            
            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipeIndex].getTopPipeY()), abs(bird.y - pipes[pipeIndex].getBottomPipeY())))
            if output[0] > .5:
                bird.jump()
            
            # drawLine(WIN, bird, pipes[pipeIndex])
        
        for i, bird in enumerate(birds):
            if checkIfOutOfScreen(settings, bg, bird, pipes) or checkCollisions(bird, pipes):
                ge[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)
        
        if len(birds) > 0:
            if checkPoints(birds[0], pipes):
                SCORE += 1
                for g in ge:
                    g.fitness += 5
        
        pygame.display.update()
        clock.tick(settings["FPS"])


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "../NEAT_config.txt")
    run(config_path)