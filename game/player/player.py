import pygame
import random

from game.player.tank import Tank
from settings import SCREEN_SIZE, PLAYER_HEIGHT, PLAYER_WIDTH


class Player:
    def __init__(self):
        max_x = SCREEN_SIZE[0] - PLAYER_WIDTH
        max_y = SCREEN_SIZE[1] - PLAYER_HEIGHT

        # Player 1 tank (Arrow keys + '0' to fire)
        self.tank1 = Tank(
            x=random.randint(0, max_x),
            y=random.randint(0, max_y),
        )

        # Player 2 tank (WASD + SPACE to fire)
        self.tank2 = Tank(
            x=random.randint(0, max_x),
            y=random.randint(0, max_y),
        )

        self.winner = None
        self.font = pygame.font.SysFont(None, 72)

    # ---------------- COLLISION: TANK vs TANK ----------------
    def check_collision(self) -> bool:
        return self.tank1.get_rect().colliderect(self.tank2.get_rect())

    # ---------------- DRAW ----------------
    def draw(self, surface):
        self.tank1.draw(surface)
        self.tank2.draw(surface)

        # If game over, show winner text
        if self.winner is not None:
            text = f"{self.winner} WINS!"
            text_surf = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(
                center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
            )
            bg_rect = text_rect.inflate(40, 20)
            pygame.draw.rect(surface, (0, 0, 0), bg_rect)
            surface.blit(text_surf, text_rect)

    # ---------------- UPDATE (MOVEMENT + BULLETS + HITS) ----------------
    def update(self):
        # If someone already won, freeze movement & bullets
        if self.winner is not None:
            return

        keys = pygame.key.get_pressed()
        speed = 1  # pixel per frame; increase/decrease if needed

        # Backup positions before movement for collision rollback
        old1 = self.tank1.rect.topleft
        old2 = self.tank2.rect.topleft

        # -------- Smooth movement: Tank 1 (Arrow keys) --------
        if keys[pygame.K_RIGHT]:
            self.tank1.rect.x += speed
            self.tank1.set_direction(180)   # right

        if keys[pygame.K_LEFT]:
            self.tank1.rect.x -= speed
            self.tank1.set_direction(0)     # left

        if keys[pygame.K_UP]:
            self.tank1.rect.y -= speed
            self.tank1.set_direction(270)   # up (your mapping)

        if keys[pygame.K_DOWN]:
            self.tank1.rect.y += speed
            self.tank1.set_direction(90)    # down (your mapping)

        # -------- Smooth movement: Tank 2 (WASD) --------
        if keys[pygame.K_d]:
            self.tank2.rect.x += speed
            self.tank2.set_direction(180)   # right

        if keys[pygame.K_a]:
            self.tank2.rect.x -= speed
            self.tank2.set_direction(0)     # left

        if keys[pygame.K_w]:
            self.tank2.rect.y -= speed
            self.tank2.set_direction(270)   # up

        if keys[pygame.K_s]:
            self.tank2.rect.y += speed
            self.tank2.set_direction(90)    # down

        # -------- Clamp tanks to stay inside the screen --------
        bounds = pygame.Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1])
        self.tank1.rect.clamp_ip(bounds)
        self.tank2.rect.clamp_ip(bounds)

        # -------- Tank vs Tank collision rollback --------
        if self.check_collision():
            self.tank1.rect.topleft = old1
            self.tank2.rect.topleft = old2
            print("Collision blocked movement!")

        # -------- Bullets & hits --------
        self.tank1.update_bullets()
        self.tank2.update_bullets()
        self.check_bullet_hits()

    # ---------------- BULLET HITS ----------------
    def check_bullet_hits(self):
        # If already someone won, skip further checks
        if self.winner is not None:
            return

        # Tank 1 bullets hitting Tank 2
        for bullet in self.tank1.bullets[:]:
            if bullet.rect.colliderect(self.tank2.get_rect()):
                print("Tank 1 WINS! Tank 2 got hit.")
                self.tank1.bullets.remove(bullet)
                self.winner = "Tank 1"
                return  # stop after win

        # Tank 2 bullets hitting Tank 1
        for bullet in self.tank2.bullets[:]:
            if bullet.rect.colliderect(self.tank1.get_rect()):
                print("Tank 2 WINS! Tank 1 got hit.")
                self.tank2.bullets.remove(bullet)
                self.winner = "Tank 2"
                return  # stop after win

    # ---------------- RESTART MATCH ----------------
    def reset_match(self):
        max_x = SCREEN_SIZE[0] - PLAYER_WIDTH
        max_y = SCREEN_SIZE[1] - PLAYER_HEIGHT

        # Respawn Tank 1
        self.tank1.rect.topleft = (
            random.randint(0, max_x),
            random.randint(0, max_y)
        )
        self.tank1.bullets.clear()
        self.tank1.direction = 90  # keep whatever base you use
        self.tank1.image = self.tank1.original_image

        # Respawn Tank 2
        self.tank2.rect.topleft = (
            random.randint(0, max_x),
            random.randint(0, max_y)
        )
        self.tank2.bullets.clear()
        self.tank2.direction = 90
        self.tank2.image = self.tank2.original_image

        # Remove winner state
        self.winner = None

        print("Match restarted!")

    # ---------------- INPUT: FIRING + RESTART ----------------
    def handle_event(self, event):

        # Allow restart when winner exists
        if self.winner is not None:
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "r":
                self.reset_match()
            return

        if event.type != pygame.KEYDOWN:
            return

        key = pygame.key.name(event.key)

        # -------- Tank 1 FIRE (0 key) --------
        if key == "0":
            self.tank1.fire()

        # -------- Tank 2 FIRE (space) --------
        elif key == "space":
            self.tank2.fire()
