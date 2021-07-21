import pygame
import random
import math

from modules.colors import colors

DEBUG = True

class Sensor():
    def __init__(self, x, y, id_):
        self.x = x
        self.y = y
        self.offset = self.setOffsetByID(id_)

    def draw(self, surface):
        pygame.draw.rect(surface, colors['white'], [self.x, self.y, 0, 0], 1)

    def setPosition(self, x, y):
        self.x, self.y = x, y

    def setDirestion(self):
        pass

    def setOffset(self, x, y):
        self.offset = (x, y)

    def setOffsetByID(self, id_):
        distance = 15

        if id_ == 0:
            return (-distance, -distance)
        elif id_ == 1:
            return (0, -distance*2)
        elif id_ == 2:
            return (distance, -distance)

    def detect(self):
        pass

class Trail():
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y

        self.strenght = 1
        self.type = type_

        self.ttlDefault = 250
        self.ttl = self.ttlDefault

        self.drawFrameDefault = 10
        self.drawFrame = self.drawFrameDefault

    def draw(self, surface):
        if self.drawFrame == self.drawFrameDefault:
            if self.type:
                pygame.draw.rect(surface, colors['searchingFood'], [self.x, self.y, 0, 0], self.strenght)
            else:
                pygame.draw.rect(surface, colors['foundFood'], [self.x, self.y, 0, 0], self.strenght)

        self.ttl -= 1
        self.drawFrame -= 1

        if self.drawFrame <= 0: self.resetDrawFrame()

    def resetTtl(self):
        self.drawFrame = self.drawFrameDefault
    
    def resetDrawFrame(self):
        self.drawFrame = self.drawFrameDefault

    def addStrenght(self):
        self.strenght += 1
        self.resetTtl()
        self.resetDrawFrame()
            
class Ant(Sensor):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 4

        self.angle = 0
        self.rotationSpeed = 15
        self.speed = 0.50
        self.distanceMax = 150

        self.tslthDefault = 120 # Time since last target hit
        self.tslth = self.tslthDefault

        self.targetPos = self.createTarget()
        self.steps = self.getSteps()

        self.searching = True
        self.sensors = [Sensor(self.x, self.y, 0), Sensor(self.x, self.y, 1), Sensor(self.x, self.y, 2)]

    def draw(self, surface):
        pygame.draw.circle(surface, colors['grey'], (self.x, self.y), self.radius)

        if DEBUG: 
            for sensor in self.sensors:
                sensor.draw(surface)

            self.drawTarget(surface)

    def drawTarget(self, surface):
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

    def checkSensors(self):
        return True
        for sensor in self.sensors:
            state = sensor.detect()
            
            if state: return state

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
        self.trailList = []

    def createAnt(self, x, y):
        self.antList.append(Ant(x, y))

    def createTrail(self, x, y, type_):
        self.trailList.append(Trail(x, y, type_))

    def draw(self):
        for ant in self.antList:
            ant.draw(self.surface)

        for trail in self.trailList:
            trail.draw(self.surface)
            if trail.ttl <= 0:
                self.trailList.remove(trail)

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
            self.createTrail(ant.x, ant.y, ant.searching)

