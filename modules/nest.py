import pygame

from modules.colors import colors
from modules.ant import AntManager

class Nest():
    def __init__(self, window, board):
        self.window = window
        self.surface = self.window.surface
        self.antManager = AntManager(self.window, board)

        self.nestX = (self.window.width-300)//2
        self.nestY = self.window.height//2 - 300
        self.radius = 12
        self.radiusHalf = self.radius/2

        self.foodDots = 0
        self.score = 0
        self.antsLiving = 0
        self.trailDots = 0
        self.antSpawnCout = 1

    def draw(self):
        pygame.draw.circle(self.surface, colors['brown'], (self.nestX, self.nestY), self.radius)
        
        textFood = self.window.font.render(f'{self.score}', False, (0, 0, 0))
        self.surface.blit(textFood,(self.nestX-self.radiusHalf+1, self.nestY-self.radiusHalf-2))

        self.antManager.draw()

    def setPosition(self, x, y):
        self.nestX, self.nestY = x, y

    def createAnts(self):
        for i in range(self.antSpawnCout):
            self.antManager.createAnt(self.nestX, self.nestY)

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


