import pygame
from pygame.locals import *

class Level_0(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Use SRCALPHA for alpha transparency
        self.rect = self.image.get_rect()
        self.rect.x = (pygame.display.Info().current_w - width) // 2
        self.rect.y = (pygame.display.Info().current_h - height) // 2
        self.color = (253, 253, 253)
        self.gap_width = 100  # Adjust the gap width as needed
        self.enemies = pygame.sprite.Group()

    def draw(self):
        # Fill the entire surface with a transparent color
        self.image.fill((0, 0, 0, 0))

        # Calculate the dimensions for the rectangles on each side
        left_rect = pygame.Rect(0, 0, self.gap_width, self.rect.height)
        right_rect = pygame.Rect(self.rect.width - self.gap_width, 0, self.gap_width, self.rect.height)

        # Draw the left and right rectangles with the background color
        pygame.draw.rect(self.image, self.color, left_rect)
        pygame.draw.rect(self.image, self.color, right_rect)