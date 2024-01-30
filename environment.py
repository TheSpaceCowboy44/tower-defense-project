import pygame
from pygame.locals import *
from constants import *
from tower import Tower

class Environment(pygame.sprite.Sprite):
    def __init__(self, enemies):
        super().__init__()
        self.towers = []
        self.enemies = []
    def draw(self, surface):
        DrawGrid(surface)
    def generateNewTower(self, player):
        self.towers.append(Tower(player))


def DrawGrid(screen):
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)