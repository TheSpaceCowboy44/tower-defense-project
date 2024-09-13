import pygame
from pygame.locals import *
from settings import *
from towers.tower_1 import Tower_1
from towers.tower_2 import Tower_2
from towers.tower_3 import Tower_3
from utils import TowerType

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.can_place_tower = True

    def update(self, current_level):
        pressed_keys = pygame.key.get_pressed()
        hasMoved = False
        
        if (pressed_keys[K_UP] or pressed_keys[K_z]) and not hasMoved:
            self.rect.y -= 5
            hasMoved = True
        if (pressed_keys[K_DOWN] or pressed_keys[K_s]) and not hasMoved:
            self.rect.y += 5
            hasMoved = True
        if (pressed_keys[K_LEFT] or pressed_keys[K_q]) and not hasMoved:
            self.rect.x -= 5
            hasMoved = True
        if (pressed_keys[K_RIGHT] or pressed_keys[K_d]) and not hasMoved:
            self.rect.x += 5
            hasMoved = True
        if hasMoved:
            self.checkWallCollision()
        if not any(pressed_keys):
            hasMoved = False
        if pressed_keys[K_1] or pressed_keys[K_2] or pressed_keys[K_3]:
            for tower_data in current_level.towerInfos:
                if tower_data.towerType == 1 and tower_data.numberOf > 0 and pressed_keys[K_1] and self.can_place_tower:
                    self.spawnTower(current_level, tower_data, TowerType.TOWER_1)
                if tower_data.towerType == 2 and tower_data.numberOf > 0 and pressed_keys[K_2] and self.can_place_tower:
                    self.spawnTower(current_level, tower_data, TowerType.TOWER_2)
                if tower_data.towerType == 3 and tower_data.numberOf > 0 and pressed_keys[K_3] and self.can_place_tower:
                    self.spawnTower(current_level, tower_data, TowerType.TOWER_3)

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
    def spawnTower(self, current_level, tower_data, tower_type):
        new_tower = Tower_1(self.rect.centerx, self.rect.centery)
        if(tower_type == TowerType.TOWER_1):
            new_tower = Tower_1(self.rect.centerx, self.rect.centery)
        if(tower_type == TowerType.TOWER_2):
            new_tower = Tower_2(self.rect.centerx, self.rect.centery)
        if(tower_type == TowerType.TOWER_3):
            new_tower = Tower_3(self.rect.centerx, self.rect.centery)
        current_level.towers.add(new_tower)
        tower_data.numberOf -= 1
        self.can_place_tower = False