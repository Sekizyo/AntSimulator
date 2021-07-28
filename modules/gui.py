import pygame

from modules.colors import colors

class Gui():
    def __init__(self, window):
        self.window = window
        self.surface = self.window.surface

        self.width = 300
        self.height = 1080

        self.x = self.window.width - self.width
        self.y = 0

        self.font = self.window.font
        self.icon_size = (48, 48)
        self.margin = 40
    
    def draw(self, nestStats, fps):
        self.drawBackground()
        self.drawStats(nestStats[0], nestStats[1], nestStats[2], fps)
        
    def drawBackground(self):
        pygame.draw.rect(self.surface, colors['black'], (self.x, self.y, self.width, self.height))

    def drawStats(self, ants=0, trail=0, food=0, fps=0):
        antsText = self.font.render(f'Ants: {ants}', False, colors['white'])

        trailText = self.font.render(f'Trail: {trail}', False, colors['white'])
        
        foodText = self.font.render(f'Food: {food}', False, colors['white'])

        fpsText = self.font.render(f'Fps: {int(fps)}', False, colors['white'])

        self.surface.blit(fpsText, (self.x+self.margin, self.y+self.margin))
        self.surface.blit(antsText, (self.x+self.margin, self.y+self.margin*2))
        self.surface.blit(trailText, (self.x+self.margin, self.y+self.margin*3))
        self.surface.blit(foodText, (self.x+self.margin, self.y+self.margin*4))