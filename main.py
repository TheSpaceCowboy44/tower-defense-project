import pygame
from pygame.locals import *
import sys
from enemy import Enemy_Type_1
from environment import Environment

from level_0 import Level_0
from constants import *
from tower import Tower

# Initialize Pygame
pygame.init()

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

        if hasMoved:
            self.checkWallCollision()

        if not any(pressed_keys):
            hasMoved = False
        
        if pressed_keys[K_e]:
            print("pressed e")
    
    def checkWallCollision(self):
        if(self.rect.x <0):
            self.rect.x = 0
        if(self.rect.x > (SCREEN_WIDTH-PLAYER_SIZE)):
            self.rect.x = SCREEN_WIDTH-PLAYER_SIZE
        if(self.rect.y <0):
            self.rect.y = 0
        if(self.rect.y > (SCREEN_HEIGHT-PLAYER_SIZE)):
            self.rect.y = SCREEN_HEIGHT-PLAYER_SIZE

# Function to spawn enemies
def spawn_enemy(enemy):
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
level_0 = Level_0(800, 600)
enemies = level_0.enemies
environment = Environment(level_0.enemies)
tower1 = Tower(100, 100)
tower2 = Tower(200, 100)
towers.add(tower1, tower2)
all_sprites.add(tower1, tower2, player, level_0)

# Game loop
running = True
spawn_timer = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn enemies every ? seconds
    now = pygame.time.get_ticks()
    for enemy in enemies:
        if now - spawn_timer > 500:
            spawn_enemy(enemy)
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
    screen.blit(level_0.image, level_0.rect.topleft)  # Draw the level on top
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()