import pygame
from pygame.locals import *
from constants import YELLOW_2
from utils import blitRotateCenter

class FakeBlock(pygame.sprite.Sprite):
    def __init__(self, angle):
        super().__init__()
        self.original_image = pygame.Surface((2, 8))
        self.original_image.fill(YELLOW_2)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(50, 50)) 
        self.angle = angle

    def update(self):
        self.angle += 1
        self.angle %= 360  
        new_image = pygame.transform.rotate(self.original_image, -self.angle)
        old_center = self.rect.center 
        self.image = new_image
        self.rect = self.image.get_rect(center=old_center) 

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
