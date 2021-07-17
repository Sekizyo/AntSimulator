import pygame
import random
import math

from modules.colors import colors

class Sensor():
    def __init__(self, x, y, id_, antRadius):
        self.x = x
        self.y = y

        self.scale = 4
        self.antRadius = antRadius
        self.radius = self.antRadius * self.scale

        self.offset = self.setOffsetByID(id_)

    def sense(self):
        pass

    def testDraw(self, surface):
        rect = pygame.draw.circle(surface, colors['white'], (self.x+self.offset[0], self.y+self.offset[1]), self.radius)

    def setPosition(self, x, y):
        self.x, self.y = x, y

    def setDirestion(self):
        pass

    def setOffset(self, x, y):
        self.offset = (x, y)

    def setOffsetByID(self, id_):
        distance = self.antRadius*self.scale

        if id_ == 0:
            return (-distance, -distance)
        elif id_ == 1:
            return (0, -distance*2)
        elif id_ == 2:
            return (distance, -distance)

class Ant(Sensor):
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y

        self.radius = 2

        self.velX = 0.0
        self.velY = 0.0

        self.angle = 0
        self.rotationSpeed = 15
        self.speed = 1

        self.targetPos = (0, 0)
        self.lastDirection = self.angle

        self.searching = True
        self.sensors = [Sensor(self.x, self.y, 0, self.radius), Sensor(self.x, self.y, 1, self.radius), Sensor(self.x, self.y, 2, self.radius)]

    def draw(self, surface):
        rect = pygame.draw.circle(surface, colors['grey'], (self.x, self.y), self.radius)
        for sensor in self.sensors:
            sensor.testDraw(surface)

    def setPosition(self, x, y):
        self.x, self.y = x, y
        for sensor in self.sensors:
            sensor.setPosition(self.x, self.y)

    def move(self):
        if self.searching:
            self.rotationSpeed = random.randint(0, 20)
            self.speed = random.randint(0, 2)
            angleNew = random.randint(0 , 360)

            self.angle = abs(self.angle - angleNew - self.rotationSpeed)

            self.velX = math.cos(self.angle) + self.speed
            self.velY = math.sin(self.angle) + self.speed

            self.setPosition(self.x + self.velX, self.y + self.velY)
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

