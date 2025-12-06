# game/player/bullet.py
import pygame

class Bullet:
    def __init__(self, x, y, speed=1, color="black", size=6):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.color = color
        self.direction = 90   # default → right

    def update(self):
        # Move based on direction
        if self.direction == 180:    # right
            self.rect.x += self.speed
        elif self.direction == 90: # up
            self.rect.y -= self.speed
        elif self.direction == 0: # left
            self.rect.x -= self.speed
        elif self.direction == 270: # down
            self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
