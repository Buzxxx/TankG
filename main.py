import pygame
from settings import SCREEN_SIZE,CAPTION
from game.game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(CAPTION)
    Game(screen=screen).run()
    pygame.quit()

if __name__ == "__main__":
    main()