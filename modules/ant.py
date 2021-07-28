import pygame
import random
import math

from modules.colors import colors

DEBUG = False

class AntManager():
    def __init__(self, window, board):
        self.window = window
        self.surface = self.window.surface
        self.board = board

        self.antList = []
        self.trailList = []

        self.radius = 4
        self.distanceMax = 50

        self.antImage = self.loadAntImage()
        self.antMask = pygame.mask.from_surface(self.antImage)

        self.targetImage = self.loadDotImage()
        self.targetMask = pygame.mask.from_surface(self.targetImage)

    def createAnt(self, x, y):
        self.antList.append(Ant(x, y, self.window, self.board))

    def createTrail(self, x, y, type_):
        self.trailList.append(Trail(x, y, type_, self.window, self.board))

    def draw(self):
        for ant in self.antList:
            ant.draw()

        if DEBUG:
            for trail in self.trailList:
                if trail.ttl <= 0:
                    self.trailList.remove(trail)
                else:
                    trail.draw()

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

            if DEBUG:
                self.createTrail(ant.x, ant.y, ant.searching)

    def loadAntImage(self):
        return pygame.image.load('modules/images/ant.png').convert_alpha()

    def loadDotImage(self):
        return pygame.image.load('modules/images/dot.png').convert_alpha()

class Ant(AntManager):
    def __init__(self, x, y, window, board):
        super().__init__(window, board)
        self.x = x
        self.y = y

        self.speed = 0.50
        self.lastDirection = 0

        self.tslthDefault = random.randint(50, 150) # Time since last target hit

        self.targetCreationTry = 1
        self.targetPos = self.createTarget()
        self.steps = self.getSteps()

        self.tslth = self.tslthDefault

        self.searching = True
        self.sensors = [Sensor(), Sensor(), Sensor()]

    def draw(self):
        self.surface.blit(self.antImage, (self.x, self.y))

        if DEBUG: 
            # for sensor in self.sensors:
            #     sensor.draw()

            self.drawTarget()

    def drawTarget(self):
        self.surface.blit(self.targetImage, self.targetPos)
        pygame.draw.line(self.surface, colors['yellow'], (self.x, self.y), self.targetPos, 1)

    def setPosition(self, x, y):
        self.x, self.y = x, y
        self.tslth -= 1

    def createTarget(self):
        self.targetCreationTry += 1
        target = (0, 0)
        
        direction = random.randint(0, 3)
        self.lastDirection = direction
        distance = self.distanceMax * (self.targetCreationTry/2)

        distanceX = random.randint(0, distance)
        distanceY = random.randint(0, distance)

        if direction == 0:
            target = (self.x + distanceX, self.y + distanceY)
        elif direction == 1:
            target = (self.x + distanceX, self.y - distanceY)
        elif direction == 2:
            target = (self.x - distanceX, self.y - distanceY)
        elif direction == 3:
            target = (self.x - distanceX, self.y + distanceY)

        target = (int(target[0]), int(target[1]))

        target = self.checkTargetColision(target)

        self.targetCreationTry = 1
        return target

    def checkTargetColision(self, target):
        if target[0] <= 0 or target[1] <= 0: # Check borders
            return self.createTarget()
        elif target[0] >= 1620 or target[1] >= 1080:
            return self.createTarget()

        elif self.board.mask.overlap(self.targetMask, target):
            return self.createTarget()
        else:
            return target
    
    def checkColission(self):
        if self.x <= 0 or self.y <= 0: # Check borders
            self.newTarget()
        elif self.x >= 1620 or self.y >= 1080:
            self.newTarget()

        if self.board.mask.overlap(self.antMask, (int(self.x), int(self.y))): 
            self.newTarget()

    def getSteps(self):
        dx, dy = (self.targetPos[0] - self.x, self.targetPos[1] - self.y)
        return (dx / 60., dy / 60.)

    def newTarget(self):
        self.targetPos = self.createTarget()
        self.steps = self.getSteps()
        self.speed = random.random() + 0.25
        self.tslth = self.tslthDefault

    def checkSensors(self):
        return True
        for sensor in self.sensors:
            state = sensor.detect()
            
            if state: return state

    def move(self):
        self.searching = self.checkSensors()

        if self.searching:
            self.setPosition(self.x + self.steps[0] * self.speed, self.y + self.steps[1] * self.speed)
            if self.tslth <= 0: self.newTarget()
        else:
            pass

        self.checkColission()

class Sensor():
    def __init__(self):
        super().__init__()

    def draw(self):
        pygame.draw.rect(self.surface, colors['white'], [self.x, self.y, 0, 0], 5)

    def detect(self):
        pass

class Trail(AntManager):
    def __init__(self, x, y, type_, window, board):
        super().__init__(window, board)
        self.x = x
        self.y = y

        self.strenght = 1
        self.type = type_

        self.ttlDefault = 50
        self.ttl = self.ttlDefault

    def draw(self):
        if self.type:
            pygame.draw.rect(self.surface, colors['searchingFood'], [self.x, self.y, 0, 0], self.strenght)
        else:
            pygame.draw.rect(self.surface, colors['foundFood'], [self.x, self.y, 0, 0], self.strenght)

        self.ttl -= 1

    def resetTtl(self):
        self.ttl = self.ttleDefault

    def addStrenght(self):
        self.strenght += 1
        self.resetTtl()
   