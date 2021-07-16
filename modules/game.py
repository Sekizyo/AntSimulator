import pygame

from modules.colors import colors
from modules.window import Window
from modules.gui import Gui
from modules.board import Board
from modules.nest import Nest

class Game():
    def __init__(self):
        self.running = True

        self.window = Window()
        self.surface = self.window.surface

        self.font = pygame.font.SysFont("arial.ttf", 75)

        self.gui = Gui(self.window)
        self.board = Board(self.window, self.gui)
        self.nest = Nest(self.window)

        self.clock = pygame.time.Clock()
        self.gameSpeed = 100
        self.fps = 60
    
    def draw(self):
        self.surface.fill(colors['background'])

        self.gui.draw()
        self.board.draw()
        self.nest.draw()

        pygame.display.update()

    def checkControls(self): # Check key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for exit button press
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT: self.running = False 
                if event.key == pygame.K_LCTRL: self.board.generateBoard() 

    def run(self):
        while self.running:
            self.checkControls()
            self.draw()
            self.clock.tick(self.fps)

def main():
    pygame.font.init()
    game = Game()
    game.run()
