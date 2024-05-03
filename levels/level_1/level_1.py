import pygame
from pygame.locals import *
from enemy import *
from levels.main_level import MainLevel, AreaBlock, getEnemyInfosFromJson, getTowerInfosFromJson

class Level_1(MainLevel):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (pygame.display.Info().current_w - width) // 2
        self.rect.y = (pygame.display.Info().current_h - height) // 2
        self.configFile = 'levels/level_1/level_1.json'
        self.enemyInfos = getEnemyInfosFromJson(self.configFile)
        self.towerInfos = getTowerInfosFromJson(self.configFile)
        self.health = 100
        self.area_blocks = getAreaBlocks()
        self.spawnEnemies()
    def update(self, player):
        super().update(player)
    def draw(self, surface):
        super().draw(surface)


def getAreaBlocks():
    area_blocks = pygame.sprite.Group()
    center_rect = pygame.Rect(SCREEN_WIDTH/2 - NORMAL_CORRIDOR_GAP, 0, SCREEN_WIDTH - (SCREEN_WIDTH/2 - NORMAL_CORRIDOR_GAP) * 2, SCREEN_HEIGHT)
    left_rect = pygame.Rect(0, 0, SCREEN_WIDTH/2 - NORMAL_CORRIDOR_GAP, SCREEN_HEIGHT)
    right_rect = pygame.Rect(SCREEN_WIDTH/2 + NORMAL_CORRIDOR_GAP, 0, SCREEN_WIDTH/2 - NORMAL_CORRIDOR_GAP, SCREEN_HEIGHT)
    
    center_block = AreaBlock(center_rect, "enemy_area", NOTVERYBLACK1)
    left_block = AreaBlock(left_rect, "tower_area", NOTVERYBLACK2)
    right_block = AreaBlock(right_rect, "tower_area", NOTVERYBLACK2)
    # center_block = AreaBlock(center_rect, "enemy_area", GREEN_GRASS_DARK)
    # left_block = AreaBlock(left_rect, "tower_area", GREEN_GRASS_LIGHT)
    # right_block = AreaBlock(right_rect, "tower_area", GREEN_GRASS_LIGHT)
    
    area_blocks.add(left_block,right_block, center_block)
    return area_blocks