import pygame
from pygame.locals import *

from constants import *

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