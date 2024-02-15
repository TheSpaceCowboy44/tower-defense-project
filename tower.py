import random
import pygame
from pygame.locals import *

from constants import *
from utils import *

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TOWER_SIZE, TOWER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.highlight_detection_circle = False
        self.bullet_images = [pygame.Surface((2, 8))]
        self.bullets = pygame.sprite.Group()
        self.spawn_bullet_timer = pygame.time.get_ticks() + 1000

    def update(self, enemies, player):
        now = pygame.time.get_ticks()
        
        enemy_detected = check_collision_group_circle(self, enemies, TOWER_1_DETECTION_RADIUS)
        if check_collision_circle(self, player, TOWER_1_DETECTION_RADIUS) or enemy_detected != False:
            self.highlight_detection_circle = True
            if enemy_detected != False and now > self.spawn_bullet_timer:
                bullet_angle = calculer_angle(self.rect.x, self.rect.y, enemy_detected.rect.x, enemy_detected.rect.y)
                bullet = TowerBullet(self, bullet_angle)
                self.bullets.add(bullet)
                self.spawn_bullet_timer = now + 1000
        else:
            self.highlight_detection_circle = False

        for bullet in self.bullets:
            bullet.update()
            if(not check_collision_circle(self, bullet, TOWER_1_DETECTION_RADIUS)):
               bullet.kill()

    def draw(self, surface):
        if self.highlight_detection_circle:
            circle_center = (self.rect.centerx, self.rect.centery)
            pygame.draw.circle(surface, GREEN, circle_center, TOWER_1_DETECTION_RADIUS, 2)

        for bullet in self.bullets:
            bullet.draw(surface)


class TowerBullet(pygame.sprite.Sprite):
    def __init__(self, tower, angle):
        super().__init__()
        self.original_image = tower.bullet_images[0]
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.image.fill(YELLOW_2)
        self.rect = self.image.get_rect(center=(tower.rect.centerx, tower.rect.centery))
        self.position = pygame.math.Vector2(tower.rect.centerx, tower.rect.centery)
        self.velocity = pygame.math.Vector2(0, 0)
        self.shooting_angle = angle
        self.move_timer = pygame.time.get_ticks() + 2000
        self.speed = 8

    def update(self):
        now = pygame.time.get_ticks()
        if now < self.move_timer:
            self.velocity.from_polar((self.speed, self.shooting_angle))
            self.position += self.velocity
            self.rect.center = (int(self.position.x), int(self.position.y))
        else:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
