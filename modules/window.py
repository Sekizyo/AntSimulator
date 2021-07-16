import pygame 

class Window():
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface((self.width, self.height))
        self.font = pygame.font.SysFont("arial.ttf", 50)
