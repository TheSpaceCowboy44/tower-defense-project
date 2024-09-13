import pygame
from pygame.locals import *
from settings import *
from utils import *

class Tower_3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TOWER_1_SIZE, TOWER_1_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.highlight_detection_circle = False
        self.laser_active = False  
        self.laser_timer = pygame.time.get_ticks() + 1000  
        self.laser_duration = 1000
        self.laser_cooldown = 1000
        self.drawLaser = False

    def update(self, enemies, player):
        now = pygame.time.get_ticks()

        enemy_detected = check_collision_group_circle(self, enemies, TOWER_1_DETECTION_RADIUS)
        if enemy_detected:
            self.highlight_detection_circle = True
            if now > self.laser_timer and not self.laser_active:
                self.laser_active = True
                self.laser_timer = now + self.laser_cooldown

        else:
            self.highlight_detection_circle = False

        if self.laser_active and now < self.laser_timer:
            angle = calculer_angle(self.rect.x, self.rect.y, enemy_detected.rect.x, enemy_detected.rect.y)
            self.drawLaser = True
        else:
            self.drawLaser = False

    def draw(self, surface):
        if self.highlight_detection_circle:
            circle_center = (self.rect.centerx, self.rect.centery)
            pygame.draw.circle(surface, GREEN, circle_center, TOWER_1_DETECTION_RADIUS, 2)
        if(self.drawLaser):
            self.draw_laser(surface)

    def draw_laser(self, surface):
        laser_width = 100  
        laser_height = 2  
        laser_color = YELLOW
        laser_rect = pygame.Rect(self.rect.centerx - laser_width // 2, self.rect.bottom, laser_width, laser_height)
        pygame.draw.rect(surface, laser_color, laser_rect)

class TowerLaser(pygame.sprite.Sprite):
    def __init__(self, tower, angle):
        super().__init__()
        self.original_image = tower.bullet_images[0]
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.image.fill(BULLET_2_COLOR)
        self.rect = self.image.get_rect(center=(tower.rect.centerx, tower.rect.centery))
        self.position = pygame.math.Vector2(tower.rect.centerx, tower.rect.centery)
        self.shooting_angle = angle