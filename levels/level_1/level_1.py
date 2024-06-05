import pygame
from pygame.locals import *
from enemy import *
from levels.main_level import AreaBlockType, MainLevel, AreaBlock, getBlockColor, getEnemyInfosFromJson, getHealthFromJson, getTowerInfosFromJson
from utils import w12,h12

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
        self.health = getHealthFromJson(self.configFile)
        self.original_health = self.health
        self.area_blocks = getAreaBlocks()
        self.route_steps = getRouteSteps()
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
            rect = pygame.Rect(x*w12(2), y*h12(2), w12(2), h12(2))
            block = AreaBlock(rect, AreaBlockType(tile), getBlockColor(tile))
            area_blocks.add(block)
    return area_blocks

def getRouteSteps():
    routeSteps = []
    routeStepsMap = getEnemyRouteMap()
    step = 1
    for y, row in enumerate(routeStepsMap):
        for x, tile in enumerate(row):
            if(int(tile) == step):
                if(step == 1):
                    isActive = True
                else:
                    isActive = False
                routeStep = EnemyRouteStep(Position((x*w12(2), (y*h12(2)))), None, isActive)
                routeSteps.append(routeStep)
                step +=1
    for i, step in enumerate(routeSteps):
        if(step[i+1] is not None):
            if(step.position.x < routeSteps[i+1].position.x):
                step.direction = Direction.RIGHT
            if(step.position.x > routeSteps[i+1].position.x):
                step.direction = Direction.LEFT
            if(step.position.y < routeSteps[i+1].position.y):
                step.direction = Direction.UP
            if(step.position.y > routeSteps[i+1].position.y):
                step.direction = Direction.DOWN
        else:
            step.direction = routeSteps[i-1].direction
    return routeSteps

def getTileMap():
    tilemap = [
        [0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ]
    return tilemap

def getEnemyRouteMap():
    route = [
        [0, 0, 1, 0, 0, 0],
        [0, 3, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 4, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 0, 0],
    ]
    return route