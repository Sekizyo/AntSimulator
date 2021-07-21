import pygame
import random
import math

from modules.colors import colors

class Sensor():
    def __init__(self, x, y, id_, antRadius):
        self.x = x
        self.y = y

        self.scale = 2
        self.antRadius = antRadius
        self.radius = self.antRadius * self.scale

        self.offset = self.setOffsetByID(id_)
        self.strenght = 0

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

    def detect(self):
        pass

class Ant(Sensor):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 2

        self.angle = 0
        self.rotationSpeed = 15
        self.speed = 0.50
        self.distanceMax = 250

        self.tslthDefault = 120
        self.tslth = self.tslthDefault # Time since last target hit

        self.targetPos = self.createTarget()
        self.steps = self.getSteps()

        self.searching = True
        self.sensors = [Sensor(self.x, self.y, 0, self.radius), Sensor(self.x, self.y, 1, self.radius), Sensor(self.x, self.y, 2, self.radius)]

    def draw(self, surface):
        pygame.draw.circle(surface, colors['grey'], (self.x, self.y), self.radius)

        for sensor in self.sensors:
            sensor.testDraw(surface)

        self.testDrawTarget(surface)

    def testDrawTarget(self, surface): #TODO DELETE
        pygame.draw.circle(surface, colors['yellow'], self.targetPos, 5)
        pygame.draw.line(surface, colors['yellow'], (self.x, self.y), self.targetPos, 1)

    def setPosition(self, x, y):
        self.x, self.y = x, y
        self.tslth -= 1
        for sensor in self.sensors:
            sensor.setPosition(self.x, self.y)

    def createTarget(self):
        target = (0, 0)
        direction = random.randint(0 , 3)
        distanceX = random.randint(0, self.distanceMax)
        distanceY = random.randint(0, self.distanceMax)


        if direction == 0:
            target = (self.x + distanceX, self.y + distanceY)
        elif direction == 1:
            target = (self.x + distanceX, self.y - distanceY)
        elif direction == 2:
            target = (self.x - distanceX, self.y - distanceY)
        elif direction == 3:
            target = (self.x - distanceX, self.y + distanceY)

        if target[0] <= 0 or target[1] <= 0:
            target = self.createTarget()
        elif target[0] >= 1620 or target[1] >= 1080:
            target = self.createTarget()
        return target

    def getSteps(self):
        dx, dy = (self.targetPos[0] - self.x, self.targetPos[1] - self.y)
        return (dx / 60., dy / 60.)

    def newTarget(self):
        self.targetPos = self.createTarget()
        self.steps = self.getSteps()
        self.speed = random.random()
        self.tslth = self.tslthDefault

    def move(self):
        self.searching = self.checkSensors()

        if self.searching:
            if int(self.x) == int(self.targetPos[0]) and int(self.y) == int(self.targetPos[1]):
                self.newTarget()
            else:
                self.setPosition(self.x + self.steps[0] * self.speed, self.y + self.steps[1] * self.speed)
                if self.tslth <= 0: self.newTarget()
        else:
            pass

class AntManager(Ant):
    def __init__(self, window):
        self.window = window
        self.surface = self.window.surface
        self.antList = []

    def createAnt(self, x, y):
        self.antList.append(Ant(x, y))

    def draw(self):
        for ant in self.antList:
            ant.draw(self.surface)

    def clearAll(self):
        self.clearAnts()
        self.clearTrail()

    def clearAnts(self):
        self.antList.clear()

    def clearTrail(self):
        self.trailList.clear()

    def moveAnts(self):
        for ant in self.antList:
            ant.move()


