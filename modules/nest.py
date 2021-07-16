import pygame

from modules.colors import colors

class Nest():
    def __init__(self, window):
        self.window = window
        self.surface = self.window.surface
        self.x = 100
        self.y = 110
        self.radius = 25
        self.radiusHalf = self.radius/2
        self.food = 0

    def draw(self):
        pygame.draw.circle(self.surface, colors['brown'], (self.x, self.y), self.radius)
        
        textFood = self.window.font.render(f'{self.food}', False, (0, 0, 0))
        self.surface.blit(textFood,(self.x-self.radiusHalf+5, self.y-self.radiusHalf-2))

    def setPosition(self, x, y):
        self.x, self.y = x, y
