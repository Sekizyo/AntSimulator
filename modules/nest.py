import pygame

from modules.colors import colors
from modules.ant import AntManager

class Nest():
    def __init__(self, window, board):
        self.window = window
        self.surface = self.window.surface
        self.antManager = AntManager(self.window, board)

        self.x = (self.window.width-300)//2
        self.y = self.window.height//2
        self.radius = 12
        self.radiusHalf = self.radius/2

        self.food = 0
        self.antCount = 30

    def draw(self):
        pygame.draw.circle(self.surface, colors['brown'], (self.x, self.y), self.radius)
        
        textFood = self.window.font.render(f'{self.food}', False, (0, 0, 0))
        self.surface.blit(textFood,(self.x-self.radiusHalf+1, self.y-self.radiusHalf-2))

        self.antManager.draw()

    def setPosition(self, x, y):
        self.x, self.y = x, y

    def createAnts(self):
        for i in range(self.antCount):
            self.antManager.createAnt(self.x, self.y)

    def clearAll(self):
        self.antManager.clearAll()

    def moveAnts(self):
        self.antManager.moveAnts()


