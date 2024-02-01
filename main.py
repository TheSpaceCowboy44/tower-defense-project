import pygame
from pygame.locals import *
import sys

from levels.level_0 import Level_0
from constants import *
from tower import Tower
from utils import MakeHud

# Initialize Pygame
pygame.init()

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.can_place_tower = True

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
        
        if pressed_keys[K_e] and self.can_place_tower:
            new_tower = Tower(player.rect.centerx, player.rect.centery)
            all_sprites.add(new_tower)
            level_0.towers.add(new_tower)
            level_0.towers_to_build -= 1
            self.can_place_tower = False
    
    def checkWallCollision(self):
        if(self.rect.x <0):
            self.rect.x = 0
        if(self.rect.x > (SCREEN_WIDTH-PLAYER_SIZE)):
            self.rect.x = SCREEN_WIDTH-PLAYER_SIZE
        if(self.rect.y <0):
            self.rect.y = 0
        if(self.rect.y > (SCREEN_HEIGHT-PLAYER_SIZE)):
            self.rect.y = SCREEN_HEIGHT-PLAYER_SIZE

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 22)

# Sprite groups
all_sprites = pygame.sprite.Group()
player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

# Create level
level_0 = Level_0(SCREEN_WIDTH, SCREEN_HEIGHT)
all_sprites.add(player)

# Game loop
running = True
spawn_timer = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()
    for enemy in level_0.enemies:
        if now - spawn_timer > 1000:
            all_sprites.add(enemy)
            spawn_timer = now

    # Update
    level_0.update(player)
    player.update()

    # Draw
    screen.fill(BLACK)
    level_0.draw(screen)
    all_sprites.draw(screen)
    screen.blit(level_0.image, level_0.rect.topleft)

    MakeHud(font, screen, level_0.enemies, level_0.towers_to_build)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()