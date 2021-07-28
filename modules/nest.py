import pygame

from modules.colors import colors
from modules.ant import AntManager

class Nest():
    def __init__(self, window, board):
        self.window = window
        self.surface = self.window.surface
        self.antManager = AntManager(self.window, board)

        self.x = (self.window.width-300)//2
        self.y = self.window.height//2 - 300
        self.radius = 12
        self.radiusHalf = self.radius/2

        self.foodDots = 0
        self.score = 0
        self.antsLiving = 0
        self.trailDots = 0
        self.antSpawnCout = 1

    def draw(self):
        pygame.draw.circle(self.surface, colors['brown'], (self.x, self.y), self.radius)
        
        textFood = self.window.font.render(f'{self.score}', False, (0, 0, 0))
        self.surface.blit(textFood,(self.x-self.radiusHalf+1, self.y-self.radiusHalf-2))

        self.antManager.draw()

    def setPosition(self, x, y):
        self.x, self.y = x, y

    def createAnts(self):
        for i in range(self.antSpawnCout):
            self.antManager.createAnt(self.x, self.y)

    def getStats(self):
        self.antsLiving = len(self.antManager.antList)
        self.trailDots = len(self.antManager.trailList)
        self.foodDots = len(self.antManager.foodList)
        return (self.antsLiving, self.trailDots, self.foodDots)

    def restart(self):
        self.antManager = AntManager(self.window, board)

    def clearAll(self):
        self.antManager.clearAll()

    def moveAnts(self):
        self.antManager.moveAnts()


