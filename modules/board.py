import random
import sys

import numpy as np
import pygame
from PIL import Image
from scipy.ndimage.interpolation import zoom

from modules.colors import colors

class Board():
    def __init__(self, window, gui):
        self.gui = gui
        self.window = window
        self.surface = self.window.surface
        
        self.x = 0
        self.y = 0
        self.width = self.window.width - self.gui.width 
        self.height = self.window.height

        self.image = self.loadMap()
        self.mask = pygame.mask.from_surface(self.image)

    def generateBoard(self):
        np.set_printoptions(threshold=sys.maxsize)

        arr = np.random.uniform(size=(8, 12))
        arr = zoom(arr, 132)
        arr = arr > 0.5
        arr = np.where(arr, 0, 1)
        arr = np.array(arr)

        new_img = Image.new('RGB', (self.width, self.height), colors['black'])

        for y, listY in enumerate(arr):
            for x, value in enumerate(listY):
                if value == 0:
                    new_img.putpixel((x, y), 0)
                else:
                    new_img.putpixel((x, y), 255)
        
        new_img.save("modules/images/map.png")
        self.image = self.loadMap()

    def createFood(self): #TODO add automatic food and nets creationx`
        pass

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))

    def loadMap(self):
        return pygame.image.load('modules/images/map.png').convert_alpha()