import random
import pygame
from pygame.locals import *

from constants import *
from utils import check_collision_circle, check_collision_group_circle

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TOWER_SIZE, TOWER_SIZE ))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self, enemies):
        if(check_collision_group_circle(self, enemies, TOWER_1_DETECTION_RADIUS)):
            bullet = TowerBullet(self)
            bullet.update()
    def draw(self, surface, player):
        if(check_collision_circle(self, player, TOWER_1_DETECTION_RADIUS)):
            circle_radius = min(self.rect.width, self.rect.height) // 2
            circle_center = (self.rect.centerx, self.rect.centery)
            pygame.draw.circle(surface, GREEN, circle_center, circle_radius, 2)


class TowerBullet(pygame.sprite.Sprite):
    def __init__(self, tower):
        super().__init__()
        self.rect = pygame.Rect(tower.rect.x, tower.rect.y, 1, 4)
        self.position = pygame.math.Vector2(tower.rect.x, tower.rect.y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = random.randrange(0,359)
        self.speed = 5
        self.move_timer = pygame.time.get_ticks() + 2000
    def update(self):
        now = pygame.time.get_ticks()
        if now < self.move_timer:
            self.velocity.from_polar((self.speed, -self.angle))
            self.position += self.velocity
            self.rect.center = (int(self.position.x), int(self.position.y))
    def draw(self, surface):
        pygame.draw.ellipse(surface, ORANGE_LIGHT, self.rect, width=0)