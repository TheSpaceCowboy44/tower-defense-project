import pygame
from pygame.locals import *
from enemy import *
from levels.main_level import MainLevel, getEnemyInfosFromJson, getHealthFromJson, getTowerInfosFromJson, getEnemyRouteFromJson, getTileMapFromJson, getAreaBlocks

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
        self.route_steps = getEnemyRouteFromJson(self.configFile)
        self.tileMap = getTileMapFromJson(self.configFile)
        self.original_health = self.health
        self.area_blocks = getAreaBlocks(self.tileMap)
        self.spawnEnemies()
    def update(self, player):
        super().update(player)
    def draw(self, surface):
        super().draw(surface)