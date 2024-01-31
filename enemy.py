import random
import pygame
from pygame.locals import *
from constants import *
from utils import Direction

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*0.05, SCREEN_WIDTH*0.05))
        self.image.fill(RED)
        self.direction = Direction.DOWN
    def update(self):
        if self.rect.y <= SCREEN_HEIGHT:
            self.rect.y += self.speed


class Enemy_Type_1(Enemy):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*0.02, SCREEN_WIDTH*0.02))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        self.speed = 1

    def update(self):
        super().update()