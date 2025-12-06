# game/player/tank.py
import pygame
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, TANK_IMAGE
from game.player.bullet import Bullet

class Tank:
    def __init__(self, x, y, image_path=TANK_IMAGE):
        # Load tank image (assumed facing RIGHT by default)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(
            self.original_image, (PLAYER_WIDTH, PLAYER_HEIGHT)
        )

        # Default facing RIGHT
        self.direction = 90

        # Current image
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))

        # Bullets list
        self.bullets = []

    # ---------------- ROTATION ----------------
    def set_direction(self, angle):
  
        self.direction = angle
        center = self.rect.center

        # Rotate by negative angle for Pygame
        self.image = pygame.transform.rotate(self.original_image, -angle)

        # Fix the rect after rotation
        self.rect = self.image.get_rect(center=center)


    # ---------------- FIRE ----------------
    def fire(self):
        # Pick spawn point based on facing direction
        if self.direction == 180:        # facing RIGHT
            bx = self.rect.right
            by = self.rect.centery
        elif self.direction == 0:        # facing LEFT
            bx = self.rect.left
            by = self.rect.centery
        elif self.direction == 270:       # facing DOWN
            bx = self.rect.centerx
            by = self.rect.bottom
        elif self.direction == 90:      # facing UP
            bx = self.rect.centerx
            by = self.rect.top
        else:
            # fallback: center
            bx = self.rect.centerx
            by = self.rect.centery

        bullet = Bullet(bx, by, speed=1)
        bullet.direction = self.direction   # keep your existing direction logic
        self.bullets.append(bullet)


    # ---------------- BULLETS ----------------
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if (bullet.rect.x < -200 or bullet.rect.x > 2000 or
                bullet.rect.y < -200 or bullet.rect.y > 2000):
                self.bullets.remove(bullet)

    def draw_bullets(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)

    # ---------------- DRAW TANK ----------------
    def get_rect(self):
        return self.rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_bullets(surface)
