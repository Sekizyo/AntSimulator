import pygame

from modules.colors import colors
from modules.window import Window
from modules.gui import Gui
from modules.board import Board
from modules.nest import Nest

class Game():
    def __init__(self, DEBUG):
        self.running = True
        self.DEBUG = DEBUG

        self.window = Window()
        self.surface = self.window.surface

        self.gui = Gui(self.window)
        self.board = Board(self.window, self.gui)
        self.nest = Nest(self.window, self.board)

        self.clock = pygame.time.Clock()
        self.gameSpeed = 100
        self.fps = 60
    
    def draw(self):
        self.surface.fill(colors['background'])

        self.gui.draw(self.nest.getStats(), self.clock.get_fps())
        self.board.draw()
        self.nest.draw()

        pygame.display.update()

    def checkControls(self): # Check key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for exit button press
                self.running = False
            
            if event.type == pygame.KEYDOWN: self.keyboardControls(event)

        self.mouseControls()

    def mouseControls(self):
        pressed = pygame.mouse.get_pressed()
        mouseX, mouseY = pygame.mouse.get_pos()

        if pressed[0]:
            self.nest.antManager.createFood(mouseX, mouseY)

        if pressed[1]:
            self.nest.setPosition(mouseX, mouseY)

    def keyboardControls(self, event):
        if event.key == pygame.K_LSHIFT: self.running = False 
        if event.key == pygame.K_SPACE: self.nest.createAnts() 
        if event.key == pygame.K_LCTRL: 
            self.nest.restart()
            self.board.generateBoard() 

    def run(self):
        if self.DEBUG:
            self.nest.createAnts()

        while self.running:
            self.checkControls()
            self.draw()
            self.nest.moveAnts()
            self.clock.tick(self.fps)

def main(DEBUG=False):
    pygame.font.init()
    game = Game(DEBUG)
    game.run()