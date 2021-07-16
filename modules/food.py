import pygame

from modules.colors import colors

class Food():
    def __init__(self, surface, id_, x, y):
        self.id = id_
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
        id_ = 0
        self.foodList.append(Food(self.surface, id_, targetX, targetY))

    def draw(self):
        for food in self.foodList:
            food.draw(self.surface)

    def getIdByPosition(self, x, y):
        for food in self.foodList:
            if food.x == x and food.y == y:
                return food.id

    def getFoodById(self, id_):
        for food in self.foodList:
            if food.id == id_:
                return food
    
    def moveFoodById(self, id_, targetX, targetY):
        food = self.getFoodById(id_)
        food.setPosition(targetX, targetY)

    def moveFoodByPosition(self, mouseX, mouseY, targetX, targetY):
        foodID = self.getIdByPosition(mouseX, mouseY)
        food = self.getFoodById(foodID)
        food.setPosition(targetX, targetY)