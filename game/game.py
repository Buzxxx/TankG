import pygame
from game.player.player import Player
from settings import SCREEN_BACKGROUND_COLOR
    
class Game():
    def __init__(self,screen):
        self.screen = screen
        self.running = True
        self.player_obj = Player()
        
    def handle_event(self,event):
        if event.type == pygame.QUIT:
            self.running =  False
        if event.type == pygame.KEYDOWN:
            self.player_obj.handle_event(event)

    def update(self):
        pygame.display.update()

    def draw(self):
        self.screen.fill(SCREEN_BACKGROUND_COLOR)
        self.player_obj.update()
        self.player_obj.draw(self.screen)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            
            self.draw()
            self.update()