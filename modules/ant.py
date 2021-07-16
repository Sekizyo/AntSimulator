import pygame
import random

from modules.colors import colors

class Ant():
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y

        self.radius = 7
        self.radiusHalf = self.radius//2

        self.velX = 0
        self.velY = 0

        self.searching = True

    def draw(self, surface):
        rect = pygame.draw.circle(surface, colors['grey'], (self.x, self.y), self.radius)

    def setPosition(self, x, y):
        self.x, self.y = x, y

    def move(self):
        if self.searching:
            self.velX += random.randint(-1, 1)
            self.velY += random.randint(-1, 1)

            self.x += self.velX
            self.y += self.velY
        else:
            pass
        
class AntManager(Ant):
    def __init__(self, window):
        self.window = window
        self.surface = self.window.surface
        self.antList = []

    def createAnt(self, targetX, targetY):
        self.antList.append(Ant(self.surface, targetX, targetY))

    def draw(self):
        for ant in self.antList:
            ant.draw(self.surface)

    def moveAnts(self):
        for ant in self.antList:
            ant.move()

