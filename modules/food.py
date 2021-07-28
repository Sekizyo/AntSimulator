import pygame

from modules.colors import colors

class FoodManager():
    def __init__(self, window):
        self.window = window
        self.surface = self.window.surface

        self.foodList = []

    def createFood(self, x, y):
        self.foodList.append(Food(x, y, self.window))

    def clearFood(self):
        self.foodList.clear()

    def getFoodCount(self):
        return len(self.foodList)
    
    def getFood(self):
        return self.foodList()

    def draw(self):
        for food in self.foodList:
            food.draw()

class Food(FoodManager):
    def __init__(self, x, y, window):
        super().__init__(window)
        self.x = x
        self.y = y
        self.radius = 2
        self.radiusHalf = self.radius//2

    def draw(self):
        pygame.draw.circle(self.surface, colors['green'], (self.x, self.y), self.radius)

    def setPosition(self, x, y):
        self.x, self.y = x, y
