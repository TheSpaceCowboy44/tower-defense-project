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
        self.highlight_detection_circle = False
        self.bullet = None
    def update(self, enemies, player):
        if(check_collision_circle(self, player, TOWER_1_DETECTION_RADIUS)):
            self.highlight_detection_circle = True
        else:
            self.highlight_detection_circle = False
        if(check_collision_group_circle(self, enemies, TOWER_1_DETECTION_RADIUS)):
            self.bullet = TowerBullet(self)
            self.bullet.update()
    def draw(self, surface):
        if self.highlight_detection_circle:
            circle_center = (self.rect.centerx, self.rect.centery)
            pygame.draw.circle(surface, GREEN, circle_center, TOWER_1_DETECTION_RADIUS, 2)


class TowerBullet(pygame.sprite.Sprite):
    def __init__(self, tower):
        super().__init__()
        self.image = pygame.Surface((3,10))
        self.image.fill(TOWER_1_BULLET_COLOR)
        self.rect = self.image.get_rect(center=(tower.centerx, tower.centery))
        self.position = pygame.math.Vector2(tower.rect.x, tower.rect.y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.angle = random.randrange(0,359)
        self.move_timer = pygame.time.get_ticks() + 5000
        self.speed = 5
    def update(self):
        now = pygame.time.get_ticks()
        if now < self.move_timer:
            self.velocity.from_polar((self.speed, -self.angle))
            self.position += self.velocity
            self.rect.center = (int(self.position.x), int(self.position.y))
            self.image = pygame.transform.rotate(self.image, self.angle)