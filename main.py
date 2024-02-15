import pygame
from pygame.locals import *
import sys

from levels.level_0 import Level_0
from constants import *
from player import Player
from utils import MakeHud

# Initialize Pygame
pygame.init()

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

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()

    # Update
    level_0.update(player)

    # Draw
    screen.fill(BLACK)
    level_0.draw(screen)
    player.draw(screen)
    screen.blit(level_0.image, level_0.rect.topleft)

    MakeHud(font, screen, level_0.enemies, level_0.towers_to_build)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()