import pygame
from pygame.locals import *
from constants import *
from tower import Tower

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.can_place_tower = True

    def update(self, level_0):
        pressed_keys = pygame.key.get_pressed()
        hasMoved = False
        
        if pressed_keys[K_UP] and not hasMoved:
            self.rect.y -= 5
            hasMoved = True
        if pressed_keys[K_DOWN] and not hasMoved:
            self.rect.y += 5
            hasMoved = True
        if pressed_keys[K_LEFT] and not hasMoved:
            self.rect.x -= 5
            hasMoved = True
        if pressed_keys[K_RIGHT] and not hasMoved:
            self.rect.x += 5
            hasMoved = True
        if hasMoved:
            self.checkWallCollision()
        if not any(pressed_keys):
            hasMoved = False
        
        if pressed_keys[K_e] and self.can_place_tower:
            new_tower = Tower(self.rect.centerx, self.rect.centery)
            level_0.towers.add(new_tower)
            level_0.towers_to_build -= 1
            self.can_place_tower = False
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def checkWallCollision(self):
        if(self.rect.x <0):
            self.rect.x = 0
        if(self.rect.x > (SCREEN_WIDTH-PLAYER_SIZE)):
            self.rect.x = SCREEN_WIDTH-PLAYER_SIZE
        if(self.rect.y <0):
            self.rect.y = 0
        if(self.rect.y > (SCREEN_HEIGHT-PLAYER_SIZE)):
            self.rect.y = SCREEN_HEIGHT-PLAYER_SIZE