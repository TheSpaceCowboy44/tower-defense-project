import pygame
from pygame.locals import *
from constants import *

# Define Button class
class Button:
    def __init__(self, text, position, size, font_size, id):
        self.text = text
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.font_size = font_size
        self.id = id
        self.background_color = GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect)
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)