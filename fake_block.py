import pygame
from pygame.locals import *
from settings import YELLOW_2
from utils import *

class FakeBlock(pygame.sprite.Sprite):
    def __init__(self, angle):
        super().__init__()
        self.image = pygame.Surface((2, 8))
        self.image.fill(YELLOW_2)
        self.rect = self.image.get_rect(center=(50, 50)) 
        self.angle = angle

    def update(self):
        self.angle += 1
        self.angle %= 360  

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        w, h = self.image.get_size()
        pos = (self.rect.centerx, self.rect.centery)
        blitRotate(surface, self.image, pos, (w/2, h/2), self.angle)
