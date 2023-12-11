import pygame
from pygame.locals import *
import sys
import random

# Initialize Pygame
pygame.init()

# Constants

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_SIZE = 400
SCREEN_WIDTH = SCREEN_SIZE
SCREEN_HEIGHT = SCREEN_SIZE
PLAYER_SIZE = SCREEN_WIDTH * 0.04
TOWER_SIZE = SCREEN_WIDTH * 0.04
ENEMY_SIZE = SCREEN_WIDTH * 0.03

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        hasMoved = False

        if pressed_keys[K_UP] and not hasMoved:
            self.rect.y -= 5
            hasMoved = True

        if pressed_keys[K_DOWN] and not hasMoved:
            self.rect.y += 5
            hasMoved = True

        if pressed_keys[K_LEFT] and not hasMoved:
            self.rect.x -= 5
            hasMoved = True

        if pressed_keys[K_RIGHT] and not hasMoved:
            self.rect.x += 5
            hasMoved = True

        self.checkWallCollision()

        if not any(pressed_keys):
            hasMoved = False
    def checkWallCollision(self):
        if(self.rect.x <0):
            self.rect.x = 0
        if(self.rect.x > (SCREEN_WIDTH-PLAYER_SIZE)):
            self.rect.x = SCREEN_WIDTH-PLAYER_SIZE
        if(self.rect.y <0):
            self.rect.y = 0
        if(self.rect.y > (SCREEN_HEIGHT-PLAYER_SIZE)):
            self.rect.y = SCREEN_HEIGHT-PLAYER_SIZE

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TOWER_SIZE, TOWER_SIZE ))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self, surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            circle_radius = min(self.rect.width, self.rect.height) // 2
            circle_center = (self.rect.centerx, self.rect.centery)
            pygame.draw.circle(surface, GREEN, circle_center, circle_radius, 2)


class Enemy_Type_1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*0.04, SCREEN_WIDTH*0.04))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(SCREEN_HEIGHT - self.rect.height)
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)

# Function to spawn enemies
def spawn_enemy():
    enemy = Enemy_Type_1()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Game")
clock = pygame.time.Clock()

# Sprite groups
all_sprites = pygame.sprite.Group()
towers = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

# Create initial towers
tower1 = Tower(100, 100)
tower2 = Tower(200, 100)
towers.add(tower1, tower2)
all_sprites.add(tower1, tower2, player)

# Game loop
running = True
spawn_timer = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn enemies every ? seconds
    now = pygame.time.get_ticks()
    if now - spawn_timer > 8000:
        spawn_enemy()
        spawn_timer = now

    # Update
    all_sprites.update()

    # Check for collisions between enemies and towers
    collisions = pygame.sprite.groupcollide(enemies, towers, False, False)
    for enemy, tower in collisions.items():
        # Do something when an enemy collides with a tower
        pass

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()