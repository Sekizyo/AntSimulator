import pygame
import random
import math

from modules.colors import colors

DEBUG = True

class AntManager():
    def __init__(self, window, board):
        self.window = window
        self.surface = self.window.surface
        self.board = board

        self.antList = []
        self.trailList = []

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
            self.manageTrailCreation(ant)

        for trail in self.trailList:
            trail.draw()
            self.manageTrailDeletion(trail)

    def manageTrailCreation(self, ant):
        if ant.lastTrailDrop <= 0:
            self.createTrail(ant.x, ant.y, ant.searching)

    def manageTrailDeletion(self, trail):
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
        self.distanceMax = 50
        self.lastDirection = 0

        self.lastTrailDropDefault = 20
        self.lastTrailDrop = 0

        self.tslthDefault = random.randint(50, 150) # Time since last target hit

        self.targetCreationTry = 1
        self.targetPos = self.createTarget()
        self.steps = self.getSteps()

        self.tslth = self.tslthDefault

        self.searching = True
        self.sensor = Sensor(self.x, self.y)

    def draw(self):
        self.surface.blit(self.antImage, (self.x, self.y))
        self.sensor.draw(self.surface)
        
        if DEBUG: 
            self.drawTarget()

    def drawTarget(self):
        self.surface.blit(self.targetImage, self.targetPos)
        pygame.draw.line(self.surface, colors['yellow'], (self.x, self.y), self.targetPos, 1)

    def setPosition(self, x, y):
        self.x, self.y = x, y
        self.tslth -= 1
        self.sensor.setPosition(x, y)

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
        self.dropTrail()
        self.sensor.detect(self.trailList)

    def dropTrail(self):
        if self.lastTrailDrop <= 0:
            self.lastTrailDrop = self.lastTrailDropDefault
        else:
            self.lastTrailDrop -= 1
        
class Sensor(Ant, AntManager):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.offset = 2.5
        self.sizeHalf = self.size//2

        self.topSensor = (0, 0, 0, 0)
        self.leftSensor = (0, 0, 0, 0)
        self.rightSensor = (0, 0, 0, 0)
        self.downSensor = (0, 0, 0, 0)
        
        self.topStrenght = 0
        self.leftStrenght = 0
        self.rightStrenght = 0
        self.downStrenght = 0

    def setPosition(self, x, y):
        self.x, self.y = x, y
        self.topSensor = (self.x-self.sizeHalf+self.offset, self.y-self.size-self.offset, self.size, self.size)
        self.leftSensor = (self.x-self.size-self.offset, self.y-self.offset, self.size, self.size)
        self.rightSensor = (self.x+self.size-self.offset, self.y-self.offset, self.size, self.size)
        self.downSensor = (self.x-self.sizeHalf+self.offset, self.y+self.size-self.offset, self.size, self.size)

    def draw(self, surface):
        pygame.draw.rect(surface, colors['searchingFood'], self.topSensor)
        pygame.draw.rect(surface, colors['searchingFood'], self.leftSensor)
        pygame.draw.rect(surface, colors['searchingFood'], self.rightSensor)
        pygame.draw.rect(surface, colors['searchingFood'], self.downSensor)

    def detect(self, trailList):
        for trail in trailList:
            if self.topSensor.colidetect(trail):
                print('##########')


class Trail(AntManager):
    def __init__(self, x, y, type_, window, board):
        super().__init__(window, board)
        self.x = x
        self.y = y

        self.strenght = 1
        self.type = type_

        self.ttlDefault = 150
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
   