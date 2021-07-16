import pygame

from modules.colors import colors

class Gui():
    def __init__(self, window):
        self.window = window
        self.surface = self.window.surface

        self.width = 300
        self.height = 1280

        self.x = self.window.width - self.width
        self.y = 0

        self.font = self.window.font
        self.icon_size = (48, 48)
        self.margin = 30
    
    def draw(self):
        self.drawBackground()
        self.drawStats()
        
    def drawBackground(self):
        pygame.draw.rect(self.surface, colors['black'], (self.x, self.y, self.width, self.height))

    def drawStats(self, ants=0):
        antsText = self.font.render(f'Ants: {ants}', False, colors['white'])
        self.surface.blit(antsText, (self.x+self.margin, self.y+self.margin))