import pygame

from modules.colors import colors
from modules.ant import AntManager

class Nest():
    def __init__(self, window, board):
        self.window = window
        self.surface = self.window.surface

        self.nestX = int((self.window.width-300)//2)
        self.nestY = int(self.window.height//2 - 300)

        self.size = 30
        self.sizeHalf = self.size//4
        self.offset = 4
        self.nestRect = pygame.Rect((self.nestX, self.nestY), (self.size, self.size))

        self.antManager = AntManager(self.window, board, self.nestRect)

        self.foodDots = 0
        self.score = 0
        self.antsLiving = 0
        self.trailDots = 0
        self.antSpawnCount = 100

    def draw(self):
        pygame.draw.rect(self.surface, colors['brown'], self.nestRect)
        
        textFood = self.window.font.render(f'{self.score}', False, (0, 0, 0))
        self.surface.blit(textFood,(self.nestX+self.sizeHalf+self.offset, self.nestY+self.sizeHalf+self.offset))

        self.antManager.draw()

    def setPosition(self, x, y):
        self.nestX, self.nestY = x, y
        self.nestRect = pygame.Rect((self.nestX, self.nestY), (self.size, self.size))

    def createAnts(self):
        for i in range(self.antSpawnCount):
            self.antManager.createAnt(self.nestX, self.nestY)

    def killAnts(self):
        try:
            for i in range(self.antSpawnCount):
                self.antManager.antList.pop(0)
        except:
            pass
        
    def getStats(self):
        self.antsLiving = len(self.antManager.antList)
        self.trailDots = len(self.antManager.trailFoundFood)
        self.foodDots = len(self.antManager.foodList)
        return (self.antsLiving, self.trailDots, self.foodDots)

    def restart(self):
        self.antManager = AntManager(self.window, board)

    def clearAll(self):
        self.antManager.clearAll()

    def moveAnts(self):
        self.antManager.moveAnts()


