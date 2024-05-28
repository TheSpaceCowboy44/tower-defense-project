import pygame
from pygame.locals import *
from enemy import *
from levels.main_level import AreaBlockType, MainLevel, AreaBlock, getBlockColor, getEnemyInfosFromJson, getHealthFromJson, getTowerInfosFromJson
from utils import h12, w12

class Level_0(MainLevel):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (pygame.display.Info().current_w - width) // 2
        self.rect.y = (pygame.display.Info().current_h - height) // 2
        self.configFile = 'levels/level_0/level_0.json'
        self.enemyInfos = getEnemyInfosFromJson(self.configFile)
        self.towerInfos = getTowerInfosFromJson(self.configFile)
        self.health = getHealthFromJson(self.configFile)
        self.original_health = self.health
        self.area_blocks = getAreaBlocks()
        self.spawnEnemies()
    def update(self, player):
        super().update(player)
    def draw(self, surface):
        super().draw(surface)



def getAreaBlocks():
    area_blocks = pygame.sprite.Group()
    tilemap = getTileMap()
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*w12(2), y*h12(2), w12(2)+1, h12(2)+1)
            block = AreaBlock(rect, AreaBlockType(tile), getBlockColor(tile))
            area_blocks.add(block)
    return area_blocks

def getTileMap():
    tilemap = [
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    ]
    return tilemap