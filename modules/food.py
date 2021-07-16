import pygame

from modules.colors import colors

class Food():
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.radiusHalf = self.radius//2

    def draw(self, surface):
        pygame.draw.circle(surface, colors['green'], (self.x, self.y), self.radius)

    def setPosition(self, x, y):
        self.x, self.y = x, y

class FoodManager(Food):
    def __init__(self, window):
        self.window = window
        self.surface = self.window.surface

        self.foodList = []

    def createFood(self, targetX, targetY):
        self.foodList.append(Food(self.surface, targetX, targetY))

    def clearFood(self):
        self.foodList.clear()

    def getFoodCount(self):
        return len(self.foodList)

    def draw(self):
        for food in self.foodList:
            food.draw(self.surface)

    def getFoodByPosition(self, x, y):
        for food in self.foodList:
            if food.x == x and food.y == y:
                return food

    def moveFoodByPosition(self, mouseX, mouseY, targetX, targetY):
        food = self.getFoodByPosition(mouseX, mouseY)
        food.setPosition(targetX, targetY)