import pygame
from pygame.locals import *

from constants import YELLOW_2

class FakeBlock(pygame.sprite.Sprite):
    def __init__(self, angle):
        super().__init__()
        self.original_image = pygame.Surface((2, 8))
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.image.fill(YELLOW_2)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.angle = angle
    def update(self):
        self.angle += 1
        new_image = pygame.transform.rotate(self.image, -self.angle)
        self.image = new_image
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)