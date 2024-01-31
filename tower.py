import random
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
    def shoot(self):
        position = pygame.math.Vector2(3, 4)
        velocity = pygame.math.Vector2(1, 0)
        position += velocity
        magnitude = position.magnitude()
        normalized_vector = position.normalize()
        #NEED TO UNDERSTAND how it works

        bullet = TowerBullet(self)

class TowerBullet(pygame.sprite.Sprite):
    def __init__(self, tower):
        super().__init__()
        self.rect = pygame.Rect(tower.rect.x, tower.rect.y, 1, 4)
        self.angle = random.randrange(0,359)
    def draw(self, surface):
        pygame.draw.ellipse(surface, ORANGE_LIGHT, self.rect, width=0)