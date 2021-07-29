import pygame
import random
import math

from modules.colors import colors

DEBUG = False

class AntManager():
    def __init__(self, window, board, nestRect):
        self.window = window
        self.surface = self.window.surface
        self.board = board

        self.antList = []
        self.foodList = []
        self.trailFoundFood = []

        self.nestRect = nestRect

        self.antImage = self.loadAntImage()
        self.antMask = pygame.mask.from_surface(self.antImage)

        self.targetImage = self.loadDotImage()
        self.targetMask = pygame.mask.from_surface(self.targetImage)

    def createAnt(self, x, y):
        self.antList.append(Ant(x, y, self.window, self.board, self.nestRect))

    def createFood(self, x, y):
        self.foodList.append(Food(x, y, self.window, self.board, self.nestRect))

    def createTrail(self, x, y, searching):
        if searching == False:
            self.trailFoundFood.append(Trail(x, y, searching, self.window, self.board, self.nestRect))

    def draw(self):
        for ant in self.antList:
            ant.draw()
            self.manageTrailCreation(ant)

        for trail in self.trailFoundFood:
            trail.draw()
            self.manageTrailDeletion(trail)

        for food in self.foodList:
            food.draw()
            self.manageFoodDeletion(food)

    def manageFoodDeletion(self, food):
        if food.strenght >= 5:
            self.foodList.remove(food)

    def manageTrailCreation(self, ant):
        if ant.lastTrailDrop <= 0:
            self.createTrail(ant.x, ant.y, ant.searching)

    def manageTrailDeletion(self, trail):
        if trail.ttl <= 0:
            if trail.type == True:
                self.trailHome.remove(trail)
            else:
                self.trailFoundFood.remove(trail)

    def clearAll(self):
        self.clearAnts()
        self.clearTrail()

    def clearAnts(self):
        self.antList.clear()

    def clearTrail(self):
        self.trailList.clear()

    def moveAnts(self):
        for ant in self.antList:
            ant.move(self.foodList, self.trailFoundFood)

    def loadAntImage(self):
        return pygame.image.load('modules/images/ant.png').convert_alpha()

    def loadDotImage(self):
        return pygame.image.load('modules/images/dot.png').convert_alpha()

class Ant(AntManager):
    def __init__(self, x, y, window, board, nestRect):
        super().__init__(window, board, nestRect)
        self.x = x
        self.y = y

        self.speed = 0.50
        self.distanceMax = 50

        self.lastTrailDropDefault = 20
        self.lastTrailDrop = 0

        self.tslthDefault = random.randint(125, 150) # Time since last target hit

        self.targetCreationTry = 1
        self.targetPos = self.createTarget()
        self.steps = self.getSteps()

        self.tslth = self.tslthDefault

        self.searching = True
        self.pickedFood = False
        self.sensor = Sensor(self.x, self.y)

    def draw(self):
        self.surface.blit(self.antImage, (self.x, self.y))
        
        if DEBUG: 
            self.drawTarget()
            self.sensor.draw(self.surface)

    def drawTarget(self):
        self.surface.blit(self.targetImage, self.targetPos)
        pygame.draw.line(self.surface, colors['yellow'], (self.x, self.y), self.targetPos, 1)

    def setPosition(self, x, y):
        self.x, self.y = x, y
        if self.searching: self.tslth -= 1
        self.sensor.setPosition(x, y)

    def updatePosition(self):
        self.x += self.steps[0] * self.speed
        self.y += self.steps[1] * self.speed
        self.sensor.setPosition(self.x, self.y)
        self.dropTrail()

        self.tslth -= 1
        if self.tslth <= 0 and self.searching: self.newTarget()

    def createTarget(self):
        self.targetCreationTry += 1
        target = (0, 0)
        
        direction = random.randint(0, 3)
        distance = self.distanceMax * (self.targetCreationTry//2)

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

    def newTarget(self, target=False):
        if target:
            self.targetPos = target
        else:
            self.targetPos = self.createTarget()

        self.steps = self.getSteps()
        self.speed = random.random()
        self.tslth = self.tslthDefault
        self.updatePosition()

    def foundFood(self):
        self.pickedFood = True
        self.searching = False

    def deliveredFood(self):
        self.pickedFood = False
        self.searching = True

    def checkSensors(self, foodList, trailFoundFood):
        target, type_ = self.sensor.detect(self.searching, foodList, trailFoundFood, self.nestRect)

        if target == None:
            return 

        elif type_ == 'food':
            self.foundFood()
            self.newTarget((self.nestRect[0], self.nestRect[1]))

        elif type_ == 'nest':
            self.deliveredFood()
            self.newTarget(target)

        elif type_ == 'trail':
            self.followTrail()

    def move(self, foodList, trailFoundFood):
        self.checkSensors(foodList, trailFoundFood)
        self.checkColission()
        self.updatePosition()

    def followTrail(self):
        pass

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
        self.sizeHalf = self.size//2
        self.offset = 2.5

        self.sensor = pygame.Rect((self.x, self.y), (self.size, self.size))
        self.lastChoice = None
        
    def setPosition(self, x, y):
        self.x, self.y = x, y
        self.sensor = pygame.Rect((self.x, self.y), (self.size, self.size))

    def draw(self, surface):
        pygame.draw.rect(surface, colors['searchingFood'], self.sensor)

    def detect(self, searchingFood, foodList, trailFoundFood, nest):
        if searchingFood:
            target = self.detectItem(foodList)
            type_ = 'food'

            if not target:
                target = self.detectItem(trailFoundFood)
                type_ = 'trail'

        else:
            target = self.detectItem([nest], True)
            type_ = 'nest'

        return target, type_

    def detectItem(self, itemList, nest=False):
        detectedItems = []
        for item in itemList:
            if self.sensor.colliderect(item):
                detectedItems.append(item)

        if detectedItems and nest:
            return detectedItems[0]

        if detectedItems:
            colidingList = []
            testList = self.sensor.collidelistall(detectedItems)

            for point in testList:
                colidingList.append(detectedItemspoint) 

            print(f'---- test - {test}')
            strongestItem = self.getStrongest(detectedItems)
            return (strongestItem.x , strongestItem.y), 

        else:
            return None

    def getStrongest(self, items):
        strongest = items[0].strenght
        stronghestItem = items[0]

        for item in items:
            if item.strenght >= strongest:
                strongest = item.strenght
                strongestItem = item

        strongestItem.addStrenght()
        return strongestItem

class Trail(AntManager):
    def __init__(self, x, y, type_, window, board, nestRect):
        super().__init__(window, board, nestRect)
        self.x = x
        self.y = y
        self.size = 1
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))

        self.type = type_

        self.strenght = 1

        self.ttlDefault = 300
        self.ttl = self.ttlDefault

    def draw(self):
        if self.type:
            pygame.draw.rect(self.surface, colors['searchingFood'], self.rect)
        else:
            pygame.draw.rect(self.surface, colors['foundFood'], self.rect)

        self.ttl -= 1

    def addStrenght(self):
        self.strenght += 1
        self.ttl = self.ttlDefault

class Food(AntManager):
    def __init__(self, x, y, window, board, nestRect):
        super().__init__(window, board, nestRect)
        self.x = x
        self.y = y

        self.strenght = 1

        self.rect = pygame.Rect((self.x, self.y), (2, 2))

    def draw(self):
        pygame.draw.rect(self.surface, colors['green'], self.rect)

    def setPosition(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect((self.x, self.y), (2, 2))

    def addStrenght(self):
        self.strenght += 1

